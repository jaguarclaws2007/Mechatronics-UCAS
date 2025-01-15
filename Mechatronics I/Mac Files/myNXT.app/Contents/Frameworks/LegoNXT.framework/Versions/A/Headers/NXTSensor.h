//
//  NXTSensor.h
//  Test
//
//  Created by Ryan Pendleton on 5/3/12.
//  Copyright (c) 2012 Inline-Studios. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "NXTDevice.h"

typedef struct {
	UInt8 port;
	UInt8 valid;
	UInt8 isCalibrated;
	UInt8 sensorType;
	SInt8 sensorMode;
	UInt16 rawValue;
	UInt16 normalizedValue;
	SInt16 scaledValue;
	SInt16 calibratedValue;
} NXTInputValues;

@interface NXTSensor : NSObject {
	NXTDevice *device;
	UInt8 port;
}

- (id)initWithPort:(UInt8)port;

//- (void)setInputMode:(NXTSensor)port type:(NXTSensorType)type mode:(NXTSensorMode)mode;
//- (NXTReturnStatus)getInputValues:(NXTInputValues*)values;
//- (void)resetInputScaledValue:(NXTSensor)aPort;

@end
