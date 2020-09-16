#include "mythreads.h"

int my_mutex_lock(my_mutex_t *mx)
{
    return pthread_mutex_lock(&mx->mx);
}

int my_mutex_unlock(my_mutex_t *mx)
{
    return pthread_mutex_unlock(&mx->mx);
}

