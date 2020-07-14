import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin';
// initialize firebase app
admin.initializeApp({
    storageBucket: "hack-covid-19-e4018.appspot.com"
});

const db = admin.firestore();

import testRegistration = require("./testRegistration");
import updateResults = require("./updateResults")

exports.testRegistration = functions.https.onCall((data, context) => {
    return testRegistration.handler(data, context, db);
});

exports.updateResults = functions.firestore.document("tests/{testId}").onUpdate((data, context) => {
    return updateResults.handler(data, context, db);
});