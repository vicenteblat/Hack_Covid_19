import * as functions from "firebase-functions"
import * as admin from 'firebase-admin';
import { TestFormData } from './test-form-data';
import { v4 as uuidv4 } from 'uuid';

const SENDGRID_API_KEY = functions.config().sendgrid.key;
const sgMail = require('@sendgrid/mail');
sgMail.setApiKey(SENDGRID_API_KEY);

export const handler = async function(data:TestFormData, context:functions.https.CallableContext, firestore: FirebaseFirestore.Firestore) {
    if (data === null) { //check for valid data
        return{
            status: 400,
            message:'No test data recieved'
        };
    }

    let testStandRef;
    const unlockCode = uuidv4()
    try { // check that the testing stand is not currently in use/valid
        const testStandSnapshot = await firestore.collection("test-stands").doc(data.testStandID).get();
        if (testStandSnapshot.exists) {
            const testStandData = testStandSnapshot.data();
            if (testStandData && testStandData.inUse) { // ignore warning, undefined is checked through exists property
                return {
                    status: 400,
                    message: "The current stand is currently processing a test, please try again later."
                }
            } else {
                testStandRef = testStandSnapshot.ref
                await testStandRef.update({
                    unlockCode: unlockCode,
                    inUse: true
                });
            }
        } else {
            return {
                status: 400,
                message: "The provided test stand ID is not valid, please try again."
            }
        }
    } catch (e) {
        return{
            status: 400,
            message: e.message
        };
    }

    let requestId = "";
    try {   //create test request entry in database
        const requestRef = await firestore.collection("tests").add({
            name: data.name,
            email: data.email,
            testStandID: data.testStandID,
            imageIDURL: data.imageIDURL
        });
        requestId = requestRef.id;
        await testStandRef.update({
            tests: admin.firestore.FieldValue.arrayUnion(requestId)
        })
    } catch (e) {
        return{
            status: 400,
            message: e.message
        };
    }

    const mssg = { //buid message for email
        to: data.email,
        from: "davidjoeful@gmail.com",
        templateId: "d-5adb5feec65f485e9cbca70c77166920",
        dynamic_template_data: {
            name: data.name,
            unlock_code: unlockCode,
        }
    }

    try { // send email to organization contact
        await sgMail.send(mssg);
        const message = 'Email sent';
        return{
            status: 200,
            message: message
        };
    } catch (e) {
        await firestore.collection("tests").doc(requestId).delete();
        return{
            status: 400,
            message: e.message
        };
    }
}