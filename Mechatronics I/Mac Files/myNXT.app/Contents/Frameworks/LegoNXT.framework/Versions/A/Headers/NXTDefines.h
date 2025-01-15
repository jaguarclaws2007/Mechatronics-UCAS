//
//  NXTDefines.h
//  LegoNXT
//
//  Created by Ryan Pendleton on 5/1/12.
//  Copyright (c) 2012 Inline-Studios. All rights reserved.
//

#define NXT_BLOCK (UInt8 command, UInt8 status, char *data, UInt16 length)
typedef void(^ConnectCallback)(BOOL success);
typedef void(^DisconnectCallback)();

typedef enum {
	kNXTDirectCommandWithReply = 0x00,
	kNXTSystemCommandWithReply = 0x01,
	kNXTReply = 0x02,
	
	kNXTDirectCommand = 0x80,
	kNXTSystemCommand = 0x81
} NXTPacketType;

typedef enum {
	kNXTRefreshInfo = 0x1,
	kNXTRefreshBattery = 0x2,
	kNXTRefreshCurrentProgram = 0x3,
	kNXTRefreshAll = (kNXTRefreshInfo | kNXTRefreshBattery | kNXTRefreshCurrentProgram)
} NXTRefreshOptions;

typedef enum {
	kNXTOpenRead = 0x80,
	kNXTOpenWrite = 0x81,
	kNXTRead = 0x82,
	kNXTWrite = 0x83,
	kNXTClose = 0x84,
	kNXTDelete = 0x85,
	kNXTFindFirst = 0x86,
	kNXTFindNext = 0x87,
	kNXTGetFirmwareVersion = 0x88,
	kNXTOpenWriteLinear = 0x89,
	kNXTOpenReadLinear = 0x8A,
	kNXTOpenWriteData = 0x8B,
	kNXTOpenAppendData = 0x8C,
	kNXTBoot = 0x97,
	kNXTSetBrickName = 0x98,
	kNXTGetInfo = 0x9B,
	kNXTDeleteUserFlash = 0xA0,
	kNXTPollLength = 0xA1,
	kNXTPoll = 0xA2,
	kNXTResetBluetooth = 0xA4
} NXTSystemCommand;

typedef enum {
	kNXTStartProgram		  = 0x00,
	kNXTStopProgram			  = 0x01,
	kNXTPlaySoundFile		  = 0x02,
	kNXTPlayTone			  = 0x03,
	kNXTSetOutputState		  = 0x04,
	kNXTSetInputMode		  = 0x05,
	kNXTGetOutputState		  = 0x06,
	kNXTGetInputValues		  = 0x07,
	kNXTResetInputScaledValue = 0x08,
	kNXTMessageWrite		  = 0x09,
	kNXTResetMotorPosition	  = 0x0A,
	kNXTGetBatteryLevel		  = 0x0B,
	kNXTStopSoundPlayback	  = 0x0C,
	kNXTKeepAlive			  = 0x0D,
	kNXTLSGetStatus			  = 0x0E,
	kNXTLSWrite				  = 0x0F,
	kNXTLSRead				  = 0x10,
	kNXTGetCurrentProgramName = 0x11,
	kNXTMessageRead			  = 0x13
} NXTDirectCommand;

typedef enum {
	kNXTNoSensor = 0x00,
	kNXTSwitch = 0x01,
	kNXTTemperature = 0x02,
	kNXTReflection = 0x03,
	kNXTAngle = 0x04,
	kNXTLightActive = 0x05,
	kNXTLightInactive = 0x06,
	kNXTSoundDB = 0x07,
	kNXTSoundDBA = 0x08,
	kNXTCustom = 0x09,
	kNXTLowSpeed = 0x0A,
	kNXTLowSpeed9V = 0x0B,
	kNXTNoOfSensorTypes = 0x0C
} NXTSensorType;

typedef enum {
	kNXTRawMode = 0x00,
	kNXTBooleanMode = 0x20,
	kNXTTransitionCntMode = 0x40,
	kNXTPeriodCounterMode = 0x60,
	kNXTPCTFullScaleMode = 0x80,
	kNXTCelciusMode = 0xA0,
	kNXTFahrenheitMode = 0xC0,
	kNXTAngleStepsMode = 0xE0,
	kNXTSlopeMask = 0x1F,
	kNXTModeMask = 0xE0
} NXTSensorMode;

typedef enum {
	kNXTSuccess = 0x00,
	kNXTNoMoreHandles = 0x81,
	kNXTNoSpace = 0x82,
	kNXTNoMoreFiles = 0x83,
	kNXTEndOfFileExpected = 0x84,
	kNXTEndOfFile = 0x85,
	kNXTNotALinearFile = 0x86,
	kNXTFileNotFound = 0x87,
	kNXTHandleAllReadyClosed = 0x88,
	kNXTNoLinearSpace = 0x89,
	kNXTUndefinedError = 0x8A,
	kNXTFileIsBusy = 0x8B,
	kNXTNoWriteBuffers = 0x8C,
	kNXTAppendNotPossible = 0x8D,
	kNXTFileIsFull = 0x8E,
	kNXTFileExists = 0x8F,
	kNXTModuleNotFound = 0x90,
	kNXTOutOfBoundary = 0x91,
	kNXTIllegalFileName = 0x92,
	kNXTIllegalHandle = 0x93,
	
	kNXTPendingCommunication = 0x20,
	kNXTMailboxEmpty = 0x40,
	kNXTRequestFailed = 0xBD,
	kNXTUnknownOpCode = 0xBE,
	kNXTInsanePacket = 0xBF,
	kNXTOutOfRange = 0xC0,
	kNXTBusError = 0xDD,
	kNXTCommunicationOverflow = 0xDE,
	kNXTChanelInvalid = 0xDF,
	kNXTChanelBusy = 0xE0,
	kNXTNoActiveProgram = 0xEC,
	kNXTIllegalSize = 0xED,
	kNXTIllegalMailbox = 0xEE,
	kNXTInvalidField = 0xEF,
	kNXTBadInputOutput = 0xF0,
	kNXTInsufficientMemmory = 0xFB,
	kNXTBadArguments = 0xFF 
} NXTReturnStatus;
