/*
  Copyright (c) 2016, Synopsys, Inc. All rights reserved worldwide.
  The information contained in this file is the proprietary and confidential
  information of Synopsys, Inc. and its licensors, and is supplied subject to,
  and may be used only by Synopsys customers in accordance with the terms and
  conditions of a previously executed license agreement between Synopsys and that
  customer.
*/

//osStatus rtos::Mutex::lock(uint32_t millisec=osWaitForever)
void _ZN4rtos5Mutex4lockEm(void)
{
    __coverity_exclusive_lock_acquire__();
}

//osStatus rtos::Mutex::unlock()
void _ZN4rtos5Mutex6unlockEv(void)
{
    __coverity_exclusive_lock_release__();
}


#if 0

typedef int TX_SEMAPHORE;
typedef int TX_MUTEX;

int tx_semaphore_get(TX_SEMAPHORE *s) {
    __coverity_semaphore_decrement__(*s);
    return 0;
}

int tx_semaphore_put(TX_SEMAPHORE *s) {
    __coverity_semaphore_increment__(*s);
    return 0;
}

int tx_mutex_get(TX_MUTEX *m, unsigned long wait_option) {
    __coverity_exclusive_lock_acquire__(*m);
    return 0;
}

int tx_mutex_put(TX_MUTEX *m) {
    __coverity_exclusive_lock_release__(*m);
    return 0;
}

#endif

