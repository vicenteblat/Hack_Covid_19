import { Injectable } from '@angular/core';
import { AngularFireStorage } from '@angular/fire/storage';
import { TestFormData } from '../interfaces/test-form-data';
import { v4 as uuidv4 } from 'node_modules/uuid';
import { TestFormResponse } from '../interfaces/test-form-response';
import { AngularFireFunctions } from '@angular/fire/functions';

@Injectable({
  providedIn: 'root'
})
export class RegisterForTestService {

  submitTestRegistration;

  constructor(private storage: AngularFireStorage, private cloud: AngularFireFunctions) { 
    this.submitTestRegistration = this.cloud.httpsCallable("testRegistration");
  }

  submitTestForm(testFormData: TestFormData, IDimage): Promise<TestFormResponse> {
    const path = "id_uploads/" + uuidv4(); //generate random uuid for each uploaded ID
    let upload = this.storage.upload(path, IDimage);
    let percentChange = upload.percentageChanges().subscribe();
    return upload.then(async snapshot => {
      percentChange.unsubscribe();
      const request = {
        name: testFormData.name,
        email: testFormData.email,
        testStandID: testFormData.testStandID,
        imageIDURL: await snapshot.ref.getDownloadURL()
      };
      return this.submitTestRegistration(request).toPromise().then(data => {
          return data
      }).catch((error) => {
        this.storage.ref(path).delete();
        return {
          status: 400,
          message: error.message
        }
      });
    }).catch(error => {
      return {
        status: 400,
        message: error.message
      }
    });
  }
}
