#pragma once


#ifdef APP_DEBUG_IO_UART
#include "debug_console_imx.h"
#endif // APP_DEBUG_IO_UART

#ifdef APP_DEBUG_IO_RPMSG
#include <proto.h>
#include <stdio.h>
#include <stdint.h>
#include "app_rpmsg.h"

void APP_Debug_IO_RPMSG_Enable();
void APP_Debug_IO_RPMSG_Send(int len);

extern uint8_t __app_io_rpmsg_buffer[0x100];
#define PRINTF(...) \
    APP_Debug_IO_RPMSG_Send(snprintf((char*)__app_io_rpmsg_buffer + 2, 0x100 - 3, __VA_ARGS__))

#endif // APP_DEBUG_IO_RPMSG
