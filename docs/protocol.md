# Dazzling2-mini UART Protocol v1

> **Status:** Draft v1.0  
> **Project:** Dazzling2-mini  
> **Author:** Pointer  
> **Last Updated:** July 2026

---

# Purpose

The Dazzling2-mini UART Protocol defines the communication standard between the two Raspberry Pi Pico 2 microcontrollers that make up the Mini Computer project.

The protocol is intended to be:

- Human readable
- Easy to debug
- Expandable
- Version controlled
- Independent of hardware implementation

The protocol will support simple one-way communication during early development and evolve into a fully bidirectional communication protocol as the project grows.

---

# Design Goals

- Simple enough to debug over a serial terminal.
- JSON-based for readability.
- Easy to expand without breaking previous versions.
- Separate communication logic from application logic.
- Allow future devices to communicate without modifying existing software.

---

# System Overview

Current hardware:

```
        UART0

+----------------+        +----------------+
| Sender Pico 2  |------->| Receiver Pico2 |
|                |        |                |
| API Fetching   |        | OLED Display   |
| Memory         |        | E-Ink Display  |
| Data Storage   |        | Rotary Encoder |
+----------------+        +----------------+
```

Current primary communication:

```
Sender  -----> Receiver
```

Future communication:

```
Sender <-----> Receiver
```

---

# Transport Layer

Interface

- UART0

Baud Rate

- 9600 baud

Encoding

- UTF-8

Packet Delimiter

```
Newline (\n)
```

GPIO Assignments (Current)

Sender

- TX -> GPIO0
- RX -> GPIO1

Receiver

- TX -> GPIO0
- RX -> GPIO1

---

# Packet Structure

Each UART packet consists of:

```
JSON
+
newline terminator
```

Example

```json
{
    "type": "data",
    "mode": "stocks",
    "data": {
        "BRK.B": {
            "price": 500.00
        }
    },
    "meta": {
        "version": 1,
        "sequence": 42
    }
}
```

Transmitted over UART as

```
{"type":"data","mode":"stocks",...}\n
```

The newline is **not** part of the JSON object.

It exists only to indicate the end of the packet.

---

# Packet Lifecycle

Sender

```
Python Dictionary
        │
        ▼
json.dumps()
        │
        ▼
JSON String
        │
        ▼
Append '\n'
        │
        ▼
.encode()
        │
        ▼
UART
```

Receiver

```
UART
        │
        ▼
Receive Bytes
        │
        ▼
Buffer
        │
        ▼
Newline Found?
        │
       Yes
        │
        ▼
Decode UTF-8
        │
        ▼
json.loads()
        │
        ▼
Python Dictionary
```

---

# Required Packet Fields

Every packet must contain the following top-level keys.

## type

Purpose

Defines what kind of packet is being transmitted.

Current packet types

```
data
request
ack
error
```

Future packet types may be added.

---

## mode

Purpose

Defines what subsystem or display mode the packet belongs to.

Current modes

```
stocks
weather
news
calendar
clock
reminders
art
diagnostics
```

Additional modes may be added without changing the protocol.

---

## data

Purpose

Contains the payload associated with the selected mode.

Examples

Stocks

```json
"data":
{
    "BRK.B":
    {
        "price":500,
        "change":0.51
    }
}
```

Weather

```json
"data":
{
    "temperature":76,
    "wind_speed":5
}
```

The internal structure of **data** depends on the selected mode.

---

## meta

Purpose

Contains protocol information rather than application data.

Current fields

```json
"meta":
{
    "version":1,
    "sequence":0
}
```

Future metadata may include

- timestamp
- sender ID
- receiver ID
- checksum
- packet size

---

# Packet Types

## data

Direction

```
Sender → Receiver
```

Purpose

Normal operating data.

Examples

- Stock information
- Weather
- Calendar
- Diagnostics

---

## request

Direction

```
Receiver → Sender
```

Purpose

Requests information.

Examples

- Request weather refresh
- Request stock history
- Request diagnostics
- Request mode change

---

## ack

Direction

```
Either Direction
```

Purpose

Confirms successful packet reception.

May be implemented in a future version.

---

## error

Direction

```
Either Direction
```

Purpose

Reports protocol or communication errors.

Examples

- Unsupported version
- Invalid JSON
- Unknown packet type
- Missing required fields

---

# Version Handling

Current protocol version

```
1
```

Receiver shall

- Read meta.version
- Compare with supported version
- Reject unsupported versions
- Log the error
- Continue operating

---

# Sequence Numbers

Every transmitted packet increments

```
meta.sequence
```

Example

```
1
2
3
4
5
```

Receiver checks sequence numbers.

Example

Received

```
10
11
13
```

Receiver logs

```
Missing packet: 12
```

Version 1 does **not** request retransmission.

Future versions may support retransmission.

---

# Receiver Operation

Receiver processing pipeline

```
Receive Bytes
        │
        ▼
Append to Buffer
        │
        ▼
Newline Found?
        │
      No │ Yes
         │
         ▼
Extract Packet
         │
         ▼
Decode UTF-8
         │
         ▼
Parse JSON
         │
         ▼
Validate Packet
         │
         ▼
Check Version
         │
         ▼
Check Sequence
         │
         ▼
Process Packet
         │
         ▼
Update Display
```

---

# Sender Operation

Sender processing pipeline

```
Collect Data
        │
        ▼
Build Dictionary
        │
        ▼
Assign Metadata
        │
        ▼
Convert to JSON
        │
        ▼
Append Newline
        │
        ▼
Encode UTF-8
        │
        ▼
Transmit UART
```

---

# Timing

Transmission timing is determined by the application.

The UART protocol itself defines **how** data is sent, not **when** it is sent.

Examples

Stocks

- Every day of the work week at noon

Weather

- Every day at noon and every other day at 6 am and pm. 

Clock

- Every second

Display refresh

- Independent of UART updates

---

# Future Expansion

Potential additions include

- Packet checksum
- CRC verification
- Packet retransmission
- Compression
- Binary payload support
- Image transfer
- File transfer
- OTA firmware updates
- Multiple receiver support
- Device discovery
- Encryption
- Authentication
- Flow control

---

# Version 1 Development Goals

Communication

- [ ] Send UTF-8 JSON
- [ ] Receive UTF-8 JSON
- [ ] Detect complete packets
- [ ] Decode JSON
- [ ] Reconstruct Python dictionary

Validation

- [ ] Validate packet type
- [ ] Validate protocol version
- [ ] Validate required fields
- [ ] Track packet sequence numbers

Application

- [ ] Display data based on mode
- [ ] Log protocol errors
- [ ] Log missing packets

---

# Revision History

## v1.0 (Draft)

Initial protocol specification.

Features

- UART communication
- JSON packet format
- UTF-8 encoding
- Newline packet delimiter
- Packet types
- Metadata
- Sequence tracking
- Bidirectional protocol planning
