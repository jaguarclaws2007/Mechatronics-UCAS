//
//  NXTBluetoothConnection.h
//  LegoNXT
//
//  Created by Ryan Pendleton on 5/1/12.
//  Copyright (c) 2012 Inline-Studios. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <IOBluetooth/IOBluetooth.h>
#import <IOBluetoothUI/IOBluetoothUI.h>

#import "NXTConnection.h"

@interface NXTBluetoothConnection : NXTConnection <IOBluetoothRFCOMMChannelDelegate> {
	IOBluetoothDevice *mBluetoothDevice;
	IOBluetoothRFCOMMChannel *mRFCOMMChannel;
}

+ (IOBluetoothDevice*)browseForDevice;

- (id)initWithBluetoothDevice:(IOBluetoothDevice*)device;

@end
