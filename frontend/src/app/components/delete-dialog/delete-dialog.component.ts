import { Component, Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-delete-dialog',
  templateUrl: './delete-dialog.component.html',
  styleUrls: ['./delete-dialog.component.css'],
})
export class DeleteDialogComponent implements OnInit {
  title: string;
  id: number;
  email: string = '';
  errMessage: string = '';
  constructor(
    private dialogRef: MatDialogRef<DeleteDialogComponent>,
    private apiService: ApiService,
    @Inject(MAT_DIALOG_DATA) data: any
  ) {
    this.title = data.title;
    this.id = data.id;
  }

  ngOnInit(): void {}

  deleteReservation() {
    this.apiService.deleteReservation(this.id, this.email).subscribe({
      next: (res) => {
        console.log(res);
        this.dialogRef.close(true);
      },
      error: (err) => {
        this.errMessage = 'Failed to delete. Did you enter the correct email?';
      },
    });
  }
}
