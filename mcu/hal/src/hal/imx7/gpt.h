#pragma once

#if !defined(HAL_IMX7)
#error "This header should be included only when building for i.MX7"
#endif

#include "FreeRTOS.h"
#include "semphr.h"

/*! @brief Available GPT instances count. */
#define HAL_GPT_INSTANCE_COUNT 2

/*! @brief Ticks per second. */
#define HAL_GPT_TICKS_PER_SECOND 6000000
