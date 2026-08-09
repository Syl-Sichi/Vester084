# Z.E.L.D.A. Android Companion

This directory defines the Android client boundary for the Z.E.L.D.A. daemon.

## Client responsibilities

* Maintain an authenticated session.
* Maintain the connection lifecycle.
* Perform HELLO and reconnect synchronization.
* Send commands and correlate responses.
* Receive events and persist the last acknowledged sequence locally.
* ACK events only after the Android client has safely accepted them.

## Protocol

The client speaks the transport frames defined by the Python daemon:

* HELLO
* SYNC
* ACK
* COMMAND
* RESPONSE
* EVENT
* ERROR
* PING
* PONG

The initial implementation deliberately keeps Android platform code separate from protocol and domain logic so the same protocol can be tested independently.
