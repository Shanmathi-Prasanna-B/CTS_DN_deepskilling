import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-student-profile',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <section>
      <h2>Student Profile</h2>
      <form [formGroup]="profileForm" (ngSubmit)="onSubmit()">
        <label>Name<input formControlName="name" /></label>
        <span *ngIf="profileForm.get('name')?.touched && profileForm.get('name')?.invalid">Name is required</span>
        <label>Email<input formControlName="email" type="email" /></label>
        <span *ngIf="profileForm.get('email')?.touched && profileForm.get('email')?.invalid">Enter a valid email</span>
        <label>Semester<input formControlName="semester" type="number" /></label>
        <button type="submit" [disabled]="profileForm.invalid">Submit</button>
      </form>
    </section>
  `,
  styles: [`
    form { display: flex; flex-direction: column; gap: 12px; max-width: 400px; }
    label { display: flex; flex-direction: column; gap: 4px; }
    span { color: #991b1b; font-size: 0.875rem; }
  `],
})
export class StudentProfileComponent {
  profileForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.profileForm = this.fb.group({
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      semester: [1, [Validators.required, Validators.min(1), Validators.max(8)]],
    });
  }

  onSubmit(): void {
    if (this.profileForm.valid) {
      console.log(this.profileForm.value);
    }
  }
}
