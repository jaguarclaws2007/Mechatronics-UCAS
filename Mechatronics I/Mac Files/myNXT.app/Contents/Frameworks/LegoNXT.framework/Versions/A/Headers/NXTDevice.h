//
//  NXTDevice.h
//  LegoNXT
//
//  Created by Ryan Pendleton on 4/27/12.
//  Copyright (c) 2012 Inline-Studios. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "NXTDefines.h"

@class NXTMotor, NXTSensor, NXTConnection;

@interface NXTDevice : NSObject {
	NXTConnection *connection;
	ConnectCallback connectCallback;
	DisconnectCallback disconnectCallback;
	
	NSString *brickName;
	NSString *bluetoothID;
	NSString *currentProgramName;
	
	UInt16 batteryLevel;
	UInt32 freeMemory;
	
	UInt8 majorFirmwareVersion;
	UInt8 minorFirmwareVersion;
	UInt8 majorProtocolVersion;
	UInt8 minorProtocolVersion;
	
	NXTMotor *motorA;
	NXTMotor *motorB;
	NXTMotor *motorC;
}

@property(copy)ConnectCallback connectCallback;
@property(copy)DisconnectCallback disconnectCallback;
@property(readonly)NXTConnection *connection;

- (id)initWithConnection:(NXTConnection*)connection;

- (void)connect;
- (void)disconnect;

- (void)didConnect;
- (void)didDisconnect;
- (void)didFailToConnect;

- (void)refresh:(BOOL)wait options:(NXTRefreshOptions)options;

#pragma mark - Brick Properties

@property(copy)NSString *brickName;
@property(copy)NSString *bluetoothID;
@property(copy)NSString *currentProgramName;

@property(readonly)UInt16 batteryLevel;
@property(readonly)UInt32 freeMemory;

@property(readonly)UInt8 majorFirmwareVersion;
@property(readonly)UInt8 minorFirmwareVersion;
@property(readonly)UInt8 majorProtocolVersion;
@property(readonly)UInt8 minorProtocolVersion;

@property(readonly)NXTMotor* motorA;
@property(readonly)NXTMotor* motorB;
@property(readonly)NXTMotor* motorC;

#pragma mark - System Commands

- (NXTReturnStatus)openRead:(NSString*)filename handle:(UInt8*)handle length:(UInt32*)fileLength;
- (NXTReturnStatus)openWrite:(NSString*)filename handle:(UInt8*)handle length:(UInt32)fileLength;

- (NXTReturnStatus)read:(UInt8)handle readLength:(UInt16)length actualLength:(UInt16*)read data:(char*)data;
- (NXTReturnStatus)write:(UInt8)handle writeLength:(UInt16)length actualLength:(UInt16*)wrote data:(char*)data;

- (NXTReturnStatus)close:(UInt8)handle;
- (NXTReturnStatus)delete:(NSString*)filename;

- (void)deleteUserFlash;

#pragma mark - Direct Commands

- (void)startProgram:(NSString*)program;
- (void)stopProgram:(NSString*)program;

- (void)playSoundFile:(NSString*)soundFile loop:(BOOL)loop;
- (void)playTone:(UInt16)tone duration:(UInt16)duration;
- (void)stopSoundPlayback;

- (void)writeMessage:(NSString*)message toInbox:(UInt8)inbox;
- (NSString*)readMessageFromInbox:(UInt8)inbox remove:(BOOL)remove;

- (void)keepAlive;
- (UInt32)getSleepTimeLimit;

@end
