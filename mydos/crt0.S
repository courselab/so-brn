.section .text
.global _start

_start:
   call get_ip_into_ax
   push %eax
   call main 
   hlt


get_ip_into_ax:
   mov 4(%esp), %eax
   ret