import { Component, Inject } from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ApiService } from 'src/app/services/api.service';
@Component({
  selector: 'app-reservation-dialog',
  templateUrl: './reservation-dialog.component.html',
  styleUrls: ['./reservation-dialog.component.css'],
})
export class ReservationDialogComponent {
  form: FormGroup;
  loading: boolean = false;
  errMessage = '';

  constructor(
    private dialogRef: MatDialogRef<ReservationDialogComponent>,
    private apiService: ApiService,
    private formBuilder: FormBuilder,

    @Inject(MAT_DIALOG_DATA) data: any
  ) {
    const startDate = data.start;
    const timezoneOffset = startDate.getTimezoneOffset(); // offset from UTC in min
    // form control needs a date local stripped after minutes, so we lose info about
    // time zone, which means we need a hacky way to show the correct local time
    const shownStartTime = new Date(
      startDate.getTime() - timezoneOffset * 60000
    );
    const shownEndTime = new Date(shownStartTime.getTime() + 30 * 60000);

    console.log(data.start);
    this.form = this.formBuilder.group({
      start: new FormControl(shownStartTime.toISOString().substring(0, 16)),
      end: new FormControl(shownEndTime.toISOString().substring(0, 16)),
      title: ['', [Validators.minLength(2), Validators.required]],
      email: ['', [Validators.required, Validators.email]],
    });
  }

  get email(): AbstractControl | null | undefined {
    return this.form?.get('email');
  }
  get title(): AbstractControl | null | undefined {
    return this.form?.get('title');
  }
  get start(): AbstractControl | null | undefined {
    return this.form?.get('start');
  }

  get end(): AbstractControl | null | undefined {
    return this.form?.get('end');
  }

  async onSubmit() {
    this.loading = true;
    if (!this.start) return;
    if (!this.end) return;
    if (!this.title) return;
    if (!this.email) return;
    this.apiService
      .postReservation({
        start: new Date(this.start.value).toISOString(),
        end: new Date(this.end.value).toISOString(),
        title: this.title.value,
        email: this.email.value,
      })
      .subscribe({
        next: (res) => {
          this.dialogRef.close(true);
          console.log(res);
        },
        error: (err) => {
          if (err.status == 422) {
            this.errMessage = err.error.detail[0].msg;
          } else {
            this.errMessage = err.error.detail;
          }
          console.log(err);
        },
      });
    this.loading = false;
  }
}
