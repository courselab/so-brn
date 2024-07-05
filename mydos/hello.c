/*
 *    SPDX-FileCopyrightText: 2024 brunoerg <brunoely.gc@gmail.com>
 *   
 *    SPDX-License-Identifier: GPL-3.0-or-later
 *
 *  This file is a derivative work from SYSeg (https://gitlab.com/monaco/syseg)
 *  and contains modifications carried out by the following author(s):
 *  brunoerg <brunoely.gc@gmail.com>
 */

#include "tydos.h"

int main()
{
  char* buf;
  gets(buf);
  puts ("Hello ");
  puts(buf);
  puts("\n");
  return 0;
}
