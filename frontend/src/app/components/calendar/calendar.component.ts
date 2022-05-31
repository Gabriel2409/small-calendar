import { Component, OnDestroy, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { CalendarEvent, CalendarView } from 'angular-calendar';
import { addDays, addHours, startOfDay } from 'date-fns';
import { Subscription } from 'rxjs';
import {
  ApiService,
  Availability,
  Reservation,
} from 'src/app/services/api.service';
import { DeleteDialogComponent } from '../delete-dialog/delete-dialog.component';
@Component({
  selector: 'mwl-demo-component',
  templateUrl: './calendar.component.html',
  styleUrls: ['./calendar.component.css'],
})
export class CalendarComponent implements OnInit, OnDestroy {
  reservations: Reservation[] = [];
  availabilities: Availability[] = [];
  reservationsSetSubscription: Subscription | null = null;
  availabilitiesSetSubscription: Subscription | null = null;

  view: CalendarView = CalendarView.Week;

  viewDate: Date = new Date();
  excludeDays: number[] = [0, 6];
  dayStartHour: number = 8;
  dayEndHour: number = 20;

  calendarEvents: CalendarEvent[] = [];

  constructor(private apiService: ApiService, private dialog: MatDialog) {}
  ngOnInit(): void {
    this._getReservations();
    this._getAvailabilities();
    this._subscribeToReservationsSet();
    this._subscribeToAvailabilitiesSet();
  }

  /**
   * Gets the reservations and emits a reservationSet event
   */
  _getReservations() {
    this.apiService.getReservations().subscribe({
      next: (res) => {
        this.apiService.reservationsSet.next(res);
      },
      error: (err) => {
        console.log(err);
      },
    });
  }

  /**
   * Gets the availabilities and emits a availabilitiesSet event
   */
  _getAvailabilities() {
    this.apiService.getAvailabilities().subscribe({
      next: (res) => {
        this.apiService.availabilitiesSet.next(res);
      },
      error: (err) => {
        console.log(err);
      },
    });
  }

  /**
   * Subscribes to the reservationSet event and updates the reservations attribute
   */
  _subscribeToReservationsSet() {
    this.reservationsSetSubscription =
      this.apiService.reservationsSet.subscribe({
        next: (res) => {
          this.reservations = res;
          console.log('reservations', this.reservations);
          this.updateEvents();
        },
        error: (err) => {
          console.log(err);
        },
      });
  }

  /**
   * Subscribes to the availabilitiesSet event and updates the availabilities attribute
   */
  _subscribeToAvailabilitiesSet() {
    this.availabilitiesSetSubscription =
      this.apiService.availabilitiesSet.subscribe({
        next: (res) => {
          this.availabilities = res;
          console.log('availabilities', this.availabilities);
        },
        error: (err) => {
          console.log(err);
        },
      });
  }

  /**
   * update shown events with the reservations
   */
  updateEvents() {
    this.calendarEvents = [];
    this.reservations.forEach((el) =>
      this.calendarEvents.push({
        id: el.id,
        start: new Date(el.start),
        end: new Date(el.end),
        title: el.title,
        actions: [
          {
            label: '<i class="fas fa-fw fa-trash"></i>Delete?',
            onClick: ({ event, sourceEvent }) => {
              this.openDeleteDialog(event);
            },
          },
        ],
      })
    );
    console.log('calendarEvents', this.calendarEvents);
  }

  /**
   * opens dialog to confirm deletion of reservation.
   */
  openDeleteDialog(calendarEvent: CalendarEvent) {
    const dialogRef = this.dialog.open(DeleteDialogComponent, {
      width: '450px',
      data: calendarEvent,
    });
    dialogRef.afterClosed().subscribe({
      next: (result: boolean | undefined) => {
        if (result === true) {
          this._getReservations();
        }
      },
    });
  }

  /**Unsubscribes from subscriptions to avoid memory leak */
  ngOnDestroy(): void {
    if (this.availabilitiesSetSubscription) {
      this.availabilitiesSetSubscription.unsubscribe();
    }
    if (this.reservationsSetSubscription) {
      this.reservationsSetSubscription.unsubscribe();
    }
  }
}
