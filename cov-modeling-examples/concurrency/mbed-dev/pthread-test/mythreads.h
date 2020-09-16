#ifndef __MYTHREADS_H__
#define __MYTHREADS_H__

#include <pthread.h>

struct my_mutex_t {
    pthread_mutex_t mx;
};

int my_mutex_lock(my_mutex_t *mx);
int my_mutex_unlock(my_mutex_t *mx);


#endif
