//
//  NXTMotor.h
//  Test
//
//  Created by Ryan Pendleton on 5/3/12.
//  Copyright (c) 2012 Inline-Studios. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "NXTDevice.h"

//typedef struct {
//	UInt8 port;
//	SInt8 power;
//	UInt8 mode;
//	UInt8 regulationMode;
//	SInt8 turnRatio;
//	UInt8 runState;
//	UInt32 tachoLimit;
//	SInt32 tachoCount;
//	SInt32 blockTachoCount;
//	SInt32 rotationCount;
//} NXTServoState;
//

typedef enum {
	kNXTServoModeCoast = 0x00,					// Coast
	kNXTServoModeOn = 0x01,						// Turn on
	kNXTServoModeBrake = 0x02,					// Use run/brake instead of run/float
	kNXTServoModeRegulated = 0x04				// Turns on the regulation
} NXTServoMode;

typedef enum {
	kNXTServoRegulationModeIdle = 0x00,			// No regulation
	kNXTServoRegulationModeMotorSpeed = 0x01,	// Power control will be enabled
	kNXTServoRegulationModeMotorSync = 0x02		// Synchronization will be enabled (needs to be enabled on two outputs)
} NXTServoRegulationMode;

typedef enum {
	kNXTServoRunStateIdle = 0x00,				// Output will be idle
	kNXTServoRunStateRampUp = 0x10,				// Output will be ramp-up
	kNXTServoRunStateRunning = 0x20,			// Output will be running
	kNXTServoRunStateRampDown = 0x40			// Output will be ramp-down
} NXTServoRunState;

typedef struct {
	UInt8 port:8;
	SInt8 power;
	NXTServoMode mode:8;
	UInt8 regulationMode;
	SInt8 turnRatio;
	UInt8 runState;
	UInt32 tachoLimit;
	SInt32 tachoCount;
	SInt32 blockTachoCount;
	SInt32 rotationCount;
} NXTServoState;

@interface NXTMotor : NSObject {
	NXTDevice *device;
	NXTServoState state;
	
	int transaction;
}

@property(readonly, nonatomic)UInt8 port;
@property(assign, nonatomic)SInt8 power;
@property(assign, nonatomic)NXTServoMode mode;
@property(assign, nonatomic)NXTServoRegulationMode regulationMode;
@property(assign, nonatomic)SInt8 turnRatio;
@property(assign, nonatomic)NXTServoRunState runState;
@property(assign, nonatomic)UInt32 tachoLimit;
@property(readonly, nonatomic)SInt32 tachoCount;
@property(readonly, nonatomic)SInt32 blockTachoCount;
@property(readonly, nonatomic)SInt32 rotationCount;

- (id)initWithPort:(UInt8)port device:(NXTDevice*)device;

- (void)beginTransaction;
- (void)flushTransaction;

- (void)process;
- (NXTReturnStatus)refresh;
- (void)resetMotorPosition;

@end
