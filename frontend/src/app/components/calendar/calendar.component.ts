import {
  ChangeDetectionStrategy,
  Component,
  OnDestroy,
  OnInit,
} from '@angular/core';
import { CalendarEvent, CalendarView } from 'angular-calendar';
import { addDays, addHours, startOfDay } from 'date-fns';
import { Subscription } from 'rxjs';
import {
  ApiService,
  Availability,
  Reservation,
} from 'src/app/services/api.service';
@Component({
  selector: 'mwl-demo-component',
  changeDetection: ChangeDetectionStrategy.OnPush,
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

  events: CalendarEvent[] = [
    {
      start: startOfDay(new Date()),
      title: 'An event',
      // color: colors.yellow,
    },
    {
      start: addHours(startOfDay(new Date()), 2),
      end: new Date(),
      title: 'Another event',
      // color: colors.blue,
    },
    {
      start: addDays(addHours(startOfDay(new Date()), 2), 2),
      end: addDays(new Date(), 2),
      title: 'And another',
      // color: colors.red,
    },
  ];

  constructor(private apiService: ApiService) {}
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
