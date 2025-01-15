//
//  NXTConnection.h
//  Test
//
//  Created by Ryan Pendleton on 5/3/12.
//  Copyright (c) 2012 Inline-Studios. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "NXTDevice.h"

@interface NXTConnection : NSObject {
	NXTDevice *device;
	
	NSThread *thread;
	NSMutableArray *callbacks;
	dispatch_queue_t queue;
	
	NSLock *callbacksLock;
	
	BOOL connected;
}

@property(assign)NXTDevice *device;
@property(readonly, getter = isConnected)BOOL connected;
- (void)connect;
- (void)disconnect;

- (void)didConnect;
- (void)didDisconnect;
- (void)didFailToConnect;

- (void)sendSystemCommand:(NXTSystemCommand)command data:(char*)data length:(UInt8)length;
- (void)sendDirectCommand:(NXTDirectCommand)command data:(char*)data length:(UInt8)length;
- (void)sendSystemCommand:(NXTSystemCommand)command data:(char*)data length:(UInt8)length callback:(void(^)NXT_BLOCK)callback;
- (void)sendDirectCommand:(NXTDirectCommand)command data:(char*)data length:(UInt8)length callback:(void(^)NXT_BLOCK)callback;
- (void)processPacket:(char*)data length:(UInt16)length;

- (void)run;
- (BOOL)writePacket:(NXTPacketType)type command:(UInt8)command data:(void*)data length:(UInt8)length;

@end
