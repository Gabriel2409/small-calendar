import {
  ChangeDetectionStrategy,
  Component,
  OnDestroy,
  OnInit,
} from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import {
  CalendarEvent,
  CalendarView,
  CalendarWeekViewBeforeRenderEvent,
} from 'angular-calendar';
import {
  addDays,
  addHours,
  addMinutes,
  hoursToMilliseconds,
  startOfDay,
} from 'date-fns';
import { Subject, Subscription } from 'rxjs';
import {
  ApiService,
  Availability,
  Reservation,
} from 'src/app/services/api.service';
import { DeleteDialogComponent } from '../delete-dialog/delete-dialog.component';
import { InstructionDialogComponent } from '../instruction-dialog/instruction-dialog.component';
import { ReservationDialogComponent } from '../reservation-dialog/reservation-dialog.component';
@Component({
  selector: 'mwl-demo-component',
  templateUrl: './calendar.component.html',
  styleUrls: ['./calendar.component.css'],
})
export class CalendarComponent implements OnInit, OnDestroy {
  reservations: Reservation[] = []; // list of all reservations
  availabilities: Availability[] = []; // list of all availabilities

  // used to determine behavior when clicking on an hour segment in the calendar.
  // tightly linked to availabilities
  availableHourSegments: Date[] = [];
  reservationsSetSubscription: Subscription | null = null; // track reservations
  availabilitiesSetSubscription: Subscription | null = null; // track availabilities

  view: CalendarView = CalendarView.Week; // show calendar week by week

  viewDate: Date = new Date(); // show current date
  excludeDays: number[] = [0, 6]; // do not show weekends
  dayStartHour: number = 6; // show only from 6am (locale time)
  dayEndHour: number = 20; // show only up to 8pm (locale time)
  hourSegments: number = 4; // divide each hour in two

  refresh = new Subject<void>(); // supposed to rerender calendar, not used, see below

  // hack to make sure the rendering occurs after retrieving the availabilities
  // seems there is a bit of an issue with this.refresh.next() not triggering
  calendarEnabled: boolean = false;

  // the list of events to show on the calendar (all the reservations)
  calendarEvents: CalendarEvent[] = [];

  constructor(private apiService: ApiService, private dialog: MatDialog) {}

  // displays instructions
  onHelpClick() {
    this.dialog.open(InstructionDialogComponent, {
      width: '450px',
    });
  }
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
   * as well as the events
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
   * + hacky way to force rerendering of the full calendar.
   */
  _subscribeToAvailabilitiesSet() {
    this.availabilitiesSetSubscription =
      this.apiService.availabilitiesSet.subscribe({
        next: (res) => {
          this.calendarEnabled = false;
          this.availabilities = res;
          console.log('availabilities', this.availabilities);
          setTimeout(() => (this.calendarEnabled = true), 50);
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
    this.reservations.forEach((el) => {
      let duration =
        (new Date(el.end).getTime() - new Date(el.start).getTime()) / 60000;
      this.calendarEvents.push({
        id: el.id,
        start: new Date(el.start),
        end: new Date(el.end),
        title: `${el.title} | ${el.email} | ${Math.floor(duration)} min`,
        actions: [
          {
            label: '<i class="fas fa-fw fa-trash"></i>Delete?',
            onClick: ({ event, sourceEvent }) => {
              this.openDeleteDialog(event);
            },
          },
        ],
      });
    });
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

  /**
   * Called each time the calendar is rendered / rerendered.
   * Changes the class of the available slots to available to allow for click events
   * on available slots only.
   * Unavailable slots appear in gray
   */
  beforeWeekViewRender(renderEvent: CalendarWeekViewBeforeRenderEvent) {
    this.availableHourSegments = [];
    const segmentLength = 1 / this.hourSegments;
    renderEvent.hourColumns.forEach((hourColumn) => {
      hourColumn.hours.forEach((hour) => {
        hour.segments.forEach((segment) => {
          for (const availability of this.availabilities) {
            let start = new Date(availability.start);
            let end = new Date(availability.end);

            if (
              addHours(segment.date, segmentLength) < end &&
              segment.date >= start
            ) {
              segment.cssClass = 'available';
              this.availableHourSegments.push(segment.date);
            }
          }
        });
      });
    });
  }

  onHourSegmentClicked(date: Date) {
    if (!this.availableHourSegments.includes(date)) return;

    const dialogRef = this.dialog.open(ReservationDialogComponent, {
      width: '450px',
      data: { start: date },
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
