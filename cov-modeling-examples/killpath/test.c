void reset(); // performs a hardware reset

int afunc()
{
    char *foo = 0;

    reset();

    *foo = 0; // null pointer deref
}

