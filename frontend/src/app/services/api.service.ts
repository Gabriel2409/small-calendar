import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  availabilities_url = '/api/availabilities';
  reservations_url = '/api/reservations';

  // when subscribing to behaviorsubjects, we get the currently stored value inside it
  // and listen to its changes
  reservationsSet = new BehaviorSubject<Reservation[]>([]);
  availabilitiesSet = new BehaviorSubject<Availability[]>([]);

  constructor(private http: HttpClient) {}

  /**
   * Gets the availability list from the backend
   */
  getAvailabilities(): Observable<Availability[]> {
    return this.http.get<Availability[]>(this.availabilities_url);
  }

  /**
   * Gets the reservation list from the backend
   */
  getReservations(): Observable<Reservation[]> {
    return this.http.get<Reservation[]>(this.reservations_url);
  }

  /**
   * Creates a new reservation
   */
  postReservation(reservation: Reservation): Observable<Reservation> {
    return this.http.post<Reservation>(this.reservations_url, reservation);
  }

  /**
   * deletes a reservation
   */
  deleteReservation(
    reservationId: number,
    reservationEmail: string
  ): Observable<Reservation> {
    return this.http.delete<Reservation>(
      `${this.reservations_url}/${reservationId}/${reservationEmail}`
    );
  }
}

/**
 * Represents a reservation. Note that we do not care about the created_at field
 */
export interface Reservation {
  id: number;
  start: string;
  end: string;
  title: string;
  email: string;
}

/**
 * Represents an availability. Note that we do not care about the created_at field
 */
export interface Availability {
  id: number;
  start: string;
  end: string;
}
