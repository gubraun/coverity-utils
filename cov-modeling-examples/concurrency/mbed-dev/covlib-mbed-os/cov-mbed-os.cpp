/*
  Copyright (c) 2016, Synopsys, Inc. All rights reserved worldwide.
  The information contained in this file is the proprietary and confidential
  information of Synopsys, Inc. and its licensors, and is supplied subject to,
  and may be used only by Synopsys customers in accordance with the terms and
  conditions of a previously executed license agreement between Synopsys and that
  customer.
*/

typedef enum {
    osNone = 0
} osStatus;

namespace rtos {
    class Mutex {

	//osStatus rtos::Mutex::lock(uint32_t millisec=osWaitForever)
	int lock(unsigned long)
	{
	    __coverity_exclusive_lock_acquire__(this);
	}

	//osStatus rtos::Mutex::unlock()
	int unlock(void)
	{
	    __coverity_exclusive_lock_release__(this);
	}
    };
}


