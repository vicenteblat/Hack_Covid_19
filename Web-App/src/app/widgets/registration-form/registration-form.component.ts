import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { RegisterForTestService } from '../../services/register-for-test.service';

@Component({
  selector: 'app-registration-form',
  templateUrl: './registration-form.component.html',
  styleUrls: ['./registration-form.component.sass']
})
export class RegistrationFormComponent implements OnInit {

  submitting = false;
  submitted = false;
  IDimage = null;
  validForm = true;
  errMessage = "";
  message = "";

  testRegistrationForm = new FormGroup({
    name: new FormControl(''),
    email: new FormControl(''),
    testStandID: new FormControl(''),
  });

  constructor(private registerForTestService: RegisterForTestService) { }

  ngOnInit(): void {
  }

  onFileChange(event) {
    if(event.target.files && event.target.files.length) {
      this.IDimage = event.target.files[0];
    }
  }

  submitForm() {
    if (this.testRegistrationForm.valid) {
      this.submitting = true;
      this.registerForTestService.submitTestForm(this.testRegistrationForm.value, this.IDimage).then((result) => {
        this.submitting = false
        this.submitted = true;
        if (result.status == 200) {
          this.message = "Thank you registering, you will receive an email shortly with information on how to administer your test."
        } else {
          this.message = result.message + " Refresh the page and try again.";
        }
      });
    } else {
      this.validForm = false;
      this.errMessage = "The form is not valid"
    }
  }
}
