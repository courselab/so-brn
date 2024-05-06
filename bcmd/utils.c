/*
 *    SPDX-FileCopyrightText: 2021 Monaco F. J. <monaco@usp.br>
 *    SPDX-FileCopyrightText: 2024 brunoerg <brunoely.gc@gmail.com>
 *   
 *    SPDX-License-Identifier: GPL-3.0-or-later
 *
 *  This file is a derivative work from SYSeg (https://gitlab.com/monaco/syseg)
 *  and contains modifications carried out by the following author(s):
 *  brunoerg <brunoely.gc@gmail.com>
 */

int __attribute__((fastcall)) strcmp(const char *s1, const char *s2)
{
  while (*s1 && *s2 && *s1 == *s2) {
    s1++;
    s2++;
  }
  return (*s1 - *s2);
}

char* __attribute__((fastcall)) contains(const char *s1, const char *s2)
{
    char* current;
    while (*s1) {
        current = (char*)s1;
        while (*current && *s2 && *current == *s2) {
            current++;
            s2++;
        }

        if (*s2 == '\0') {
            return (char*)s1;
        }

        s1++;
        s2 = s2 - (current - (char*)s1);
    }	
    return NULL;	
}



