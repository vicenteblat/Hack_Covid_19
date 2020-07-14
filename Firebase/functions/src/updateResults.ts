import * as functions from 'firebase-functions';

const SENDGRID_API_KEY = functions.config().sendgrid.key;
const sgMail = require('@sendgrid/mail');
sgMail.setApiKey(SENDGRID_API_KEY);

export const handler = async function(data: any, context: functions.EventContext, firestore: FirebaseFirestore.Firestore) {
    const testId = context.params.testId;
    let testSnapshot;
    try {
        testSnapshot = await firestore.collection("tests").doc(testId).get()
    } catch (e) {
        return {
            status: 400,
            message: "There was an error getting the test data"
        }
    }

    const testData = testSnapshot.data();
    if (testData) {
        const mssg = { //buid message for email
            to: testData.email,
            from: "davidjoeful@gmail.com",
            templateId: testData.result ? "d-9d4d4641ebaa4330ac73dfba41fbaab9" : "d-4450d7f70b5a41e9b370f6a451456c60",
            dynamic_template_data: {
                name: testData.name,
            }
        }
        try {
            await sgMail.send(mssg);
            const message = 'Email sent';
            return{
                status: 200,
                message: message
            };
        } catch (e) {
            return{
                status: 400,
                message: e.message
            };
        }
    } else {
        return {
            status: 400,
            message: "There was a problem getting the test data."
        }
    }
}