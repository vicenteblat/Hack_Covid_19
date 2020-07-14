import { TestBed } from '@angular/core/testing';

import { RegisterForTestService } from './register-for-test.service';

describe('RegisterForTestService', () => {
  let service: RegisterForTestService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RegisterForTestService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
