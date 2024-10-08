#    SPDX-FileCopyrightText: 2021 Monaco F. J. <monaco@usp.br>
#    SPDX-FileCopyrightText: 2024 brunoerg <brunoely.gc@gmail.com>
#   
#    SPDX-License-Identifier: GPL-3.0-or-later
#
#  This file is a derivative work from SYSeg (https://gitlab.com/monaco/syseg)
#  and contains modifications carried out by the following author(s):
#  brunoerg <brunoely.gc@gmail.com>

###########################################################
##
## These are the rules of interest in this set of examples.
##



# By default, the bootable program name will by $(dosname).bin
# If you export this directory to extend the example as part of a programming
# exercise, redefine $(dos) to reflect your own DOS name, say
# dos = "amazingOS" 

dos= "idos"

# Build the OS and an example user program.

all: $(dos).bin prog.bin hello.bin

# Create a 1.44 MB floppy image (2880 * 512 bytes)

disk.img:
	rm -f $@
	dd if=/dev/zero of=$@ count=2880

# Link all objects needed by the OS.

$(dos).bin : bootloader.o bios1.o kernel.o kaux.o bios2.o logo.o syscall.o 
	ld -melf_i386 -T tydos.ld --orphan-handling=discard $^ -o $@

# Here we are statically linking the user program 'prob.bin' into the kernel,
# so as to simulate the execution of a user program. If we were to actually load
# and execute an external program, we should remove 'prog.o' and 'libtydos.o'
# from the list of pre-requisites, and edit the linker script accordingly.
# Comment out the following line if this is the case.

# $(dos).bin : prog.o libtydos.o 

# Rules to build objects from either C or assembly code.

%.o : %.c
	gcc -m16 -O0 --freestanding -fno-pic -fcf-protection=none -c $(CFLAGS) $< -o $@

%.o : %.S
	as -32 $< -o $@

bootloader.o : bios1.h kernel.h 
kernel.o : bios1.h bios2.h kernel.h kaux.h   
kaux.o:    bios2.h kaux.h   

$(dos).bin : .EXTRA_PREREQS = rt0.o tydos.ld

# Rules to build the user programs
# You would add new programs to this variable if bulding other user programs.
# The user library is automatically added by the linker script.

progs = prog.bin

$(progs)  : %.bin : %.o libtydos.a 
	ld -melf_i386 -T prog.ld --orphan-handling=discard crt0.o $< libtydos.a -o $@

$(progs:%.bin=%.o) : %.o : %.c tydos.h
	gcc -m16 -O0 --freestanding -fno-pic -fcf-protection=none -c $(CFLAGS) $< -o $@

$(progs:%.bin=%.o) : tydos.h

$(progs:%.bin=%.o) : .EXTRA_PREREQS = prog.ld

# Hello

hellos = hello.bin

$(hellos)  : %.bin : %.o libtydos.a 
	ld -melf_i386 -T prog.ld --orphan-handling=discard crt0.o $< libtydos.a -o $@

$(hellos:%.bin=%.o) : %.o : %.c tydos.h
	gcc -m16 -O0 --freestanding -fno-pic -fcf-protection=none -c $(CFLAGS) $< -o $@

$(hellos:%.bin=%.o) : tydos.h

$(hellos:%.bin=%.o) : .EXTRA_PREREQS = tydos.ld

# Recipes to build the user library.

libtydos.o: libtydos.c tydos.h
	gcc -m16 -O0 --freestanding -fno-pic -fcf-protection=none -c $(CFLAGS) $< -o $@

libtydos.o : tydos.h

libtydos.a : libtydos.o
	ar rcs $@ $^

# Housekeeping.

.PHONY: clean

clean:
	rm -f *.bin *.o *~ *.s *.a


## Bintools: convenience rules for inspecting binary files
##
## SYSeg's Bintools is a collection of Makefile rules for invoking
## binary-inspection utility programs. It contains handy shortcuts for
## disassembling objects, comparing files, creating bootable images, invoking
## platform emulators and other facilities. Some shortcuts are ad hoc rules
## crafted under a poetic license and may depart from conventional Make usage.

##
## Configuration
##


# Inform your preferred graphical diff tool e.g meld, kdiff3 etc.

DIFF_TOOL=meld


##
## You probably don't need to change beyond this line
##

# Disassemble

# ALT = intel | att  (default: att)

ifndef ASM
ifeq (,$(findstring intel, $(MAKECMDGOALS)))
ASM_SYNTAX = att
else
ASM_SYNTAX = intel
endif
else
ASM_SYNTAX= $(ASM)
endif

# BIT = 16 | 32  (default: 32)

ifndef BIT
ifeq (,$(findstring 16, $(MAKECMDGOALS)))
ASM_MACHINE = i386
else
ASM_MACHINE = i8086
endif
else

ifeq ($(BIT),16)
ASM_MACHINE = i8086
else
ASM_MACHINE = i386
endif

endif


intel att 16 32: 
	@echo > /dev/null

##
## Options
##

opts = $(filter .optnop, $(MAKECMDGOALS))
symbol = $(filter ..%, $(MAKECMDGOALS))

$(opts) $(symbol):
	@echo > /dev/null

objdump_nop = "cat"
objdump_disassemble = "-d"

#
# Disassemble options
#

ifneq (,$(filter d diss d* diss*, $(MAKECMDGOALS)))


ifneq (,$(findstring .optnop, $(opts)))
objdump_nop = "sed 's/:\(\t.*\t\)/:    /g'"
endif

ifneq (,$(symbol))
objdump_disassemble = "--disassemble=$(symbol:..%=%)"
endif

endif


#
# Disassemble
#

diss d diss* d* : baz=$(bar)

diss d diss* d*: $(IMG) 
	@objdump -f $< > /dev/null 2>&1; \
	if test $$? -eq 1   ; then \
	  objdump -M $(ASM_SYNTAX) -b binary -m $(ASM_MACHINE) -D $< | "$(objdump_nop)"; \
	else \
	  if test $@ = "diss" || test $@ = "d" ; then\
	   objdump -M $(ASM_SYNTAX) -m $(ASM_MACHINE) $(objdump_disassemble) $<  | "$(objdump_nop)" ;\
	  else\
	    objdump -M $(ASM_SYNTAX) -m $(ASM_MACHINE) -D $< | "$(objdump_nop)" ; \
	 fi;\
	fi

%/diss %/d %/diss* %/d*: %
	make $(@F) IMG=$< $(filter 16 32 intel att $(opts) $(symbol), $(MAKECMDGOALS)) 

%/i16 %/16i : %
	make --quiet $</diss intel 16 $(opts) $(symbol)
%/i32 %/32i %/i: %
	make --quiet $</diss intel 32 $(opts) $(symbol)
%/a16 %/16a %/16 : %
	make --quiet $</diss att 16 $(opts) $(symbol)
%/a32 %/32a %/32 %/a: %
	make --quiet $</diss att 32 $(opts) $(symbol)

%/i16* %/16i* : %
	make --quiet $</diss* intel 16 $(opts) $(symbol)
%/i32* %/32i* %/i*: %
	make --quiet $</diss* intel 32 $(opts) $(symbol)
%/a16* %/16a* %/16* : %
	make --quiet $</diss* att 16 $(opts) $(symbol)
%/a32* %/32a* %/32* %/a*: %
	make --quiet $</diss* att 32 $(opts) $(symbol)

%/less : %
	less $(@D)

%/cat : %
	cat $(@D)

##
## Run on the emulator
##

# 
#
# %/run : %
# 	@i=$< &&\
# 	if test $${i##*.} = "img"; then\
# 	    make run-fd IMG=$<;\
# 	 else\
# 	   if test $${i##*.} = "bin"; then\
# 	     make run-bin IMG=$<;\
# 	    fi;\
# 	fi
#
# %/bin : %
# 	make run-bin IMG=$<
#
# %/fd : %
# 	make run-fd IMG=$<

%/run : %
	make run IMG=$<

run: $(IMG)
	qemu-system-i386 -drive format=raw,file=$< -net none

# These are deprecate; use %/run, instead.

run-bin: $(IMG)
	qemu-system-i386 -drive format=raw,file=$< -net none
	@echo "Shortcut run-bin is deprecated: use 'make run' instead."

run-iso: $(IMG)
	qemu-system-i386 -drive format=raw,file=$< -net none
	@echo "Shortcut run-iso is deprecated: use 'make run' instead."

run-fd : $(IMG)
	qemu-system-i386 -drive format=raw,file=$< -net none
	@echo "Shortcut run-fd is deprecated: use 'make run' instead."



# Dump contents in hexadecimal

hex raw dump: $(IMG)
	hexdump -C $<


%/hex %raw %/dump : %
	make --quiet dump IMG=$< 


# Diff-compare


MISSING_DIFF_TOOL="Can't find $(DIFF_TOOL); please edit syseg/tools/bintools.m4"

# Compare objects

objdiff bindiff : $(wordlist 2, 4, $(MAKECMDGOALS))
	if  test -z $$(which $(DIFF_TOOL)); then echo $(MISSING_DIFF_TOOL); exit 1; fi
	if test $(words $^) -lt 4 ; then\
	  bash -c "$(DIFF_TOOL) <(make $(wordlist 1,1,$^)/diss $(ASM) $(BIT)) <(make $(wordlist 2,2,$^)/diss $(ASM) $(BIT))";\
	else\
	  bash -c "$(DIFF_TOOL) <(make $(wordlist 1,1,$^)/diss $(ASM) $(BIT)) <(make $(wordlist 2,2,$^)/diss $(ASM) $(BIT)) <(make $(wordlist 3,3,$^)/diss $(ASM) $(BIT))";\
	fi

# Compare sources

srcdiff : $(wordlist 2, 4, $(MAKECMDGOALS))
	if  test -z $$(which $(DIFF_TOOL)); then echo $(MISSING_DIFF_TOOL); exit 1; fi
	if test $(words $^) -lt 3 ; then\
	  bash -c "$(DIFF_TOOL) $(wordlist 1,1,$^) $(wordlist 2,2,$^)";\
	else\
	  bash -c "$(DIFF_TOOL) $(wordlist 1,1,$^) $(wordlist 2,2,$^) $(wordlist 3,3,$^)";\
	fi

# Compare hex

hexdiff : $(wordlist 2, 4, $(MAKECMDGOALS))
	if  test -z $$(which $(DIFF_TOOL)); then echo $(MISSING_DIFF_TOOL); exit 1; fi
	if test $(words $^) -lt 4 ; then\
	  bash -c "$(DIFF_TOOL) <(make $(wordlist 1,1,$^)/hex $(ASM) $(BIT)) <(make $(wordlist 2,2,$^)/hex $(ASM) $(BIT))";\
	else\
	  bash -c "$(DIFF_TOOL) <(make $(wordlist 1,1,$^)/hex $(ASM) $(BIT)) <(make $(wordlist 2,2,$^)/hex $(ASM) $(BIT)) <(make $(wordlist 3,3,$^)/hex $(ASM) $(BIT))";\
	fi


# Compare objects and sources

diff : $(word 2, $(MAKECMDGOALS))
	@echo $(wordlist 2, 4, $(MAKECMDGOALS))
	@EXT=$(suffix $<);\
	case $$EXT in \
	.bin | .o)\
		make --quiet objdiff $(wordlist 2, 4, $(MAKECMDGOALS))\
		;;\
	.asm | .S | .s | .i | .c | .h | .hex)\
		make --quiet srcdiff $(wordlist 2, 4, $(MAKECMDGOALS))\
		;;\
	.img )\
		make --quiet hexdiff $(wordlist 2, 4, $(MAKECMDGOALS))\
		;;\
	*)\
		echo "I don't know how to compare filetype $$EXT"\
		;;\
	esac


# Choose between intel|att and 16-bit|32-bot

diffi16 di16 i16:
	make --quiet diff $(wordlist 2, 4, $(MAKECMDGOALS)) ASM=intel BIT=16

diffi32 di32 i32:
	make --quiet diff $(wordlist 2, 4, $(MAKECMDGOALS)) ASM=intel BIT=32

diffa16 da16 a16:
	make --quiet diff $(wordlist 2, 4, $(MAKECMDGOALS)) ASM=att BIT=16

diffa32 da32 a32:
	make --quiet diff $(wordlist 2, 4, $(MAKECMDGOALS)) ASM=att BIT=32

##
## Copy bin to img
##

BIN_FILE := idos.bin
DISK_IMG := disk.img
HEADER_SIZE := 62

copy_bin_img:
	dd conv=notrunc ibs=1 obs=1 skip=62 seek=62 if=$(BIN_FILE) of=$(DISK_IMG)

# End of Bintools.
# -------------------------------------------------------------



EXPORT_FILES = Makefile README bootloader.c kernel.c kernel.h kaux.c kaux.h bios1.S bios1.h bios2.S bios2.h syscall.c tydos.ld  libtydos.c tydos.h tydos.h prog.c prog.ld hello.c rt0.S  logo.c
EXPORT_NEW_FILES = NOTEBOOK


## Export rules.
## These rules are not relevant for the exercise.
## They are used by SYSeg to create a self-contained distribution bundle
## of the source directory, suitable for exporting project files.

TARNAME=$(dos)


syseg-export export:
	@if test -f .dist; then\
	  echo "This is an exported bundle already. Nothing to be done.";\
	  exit 0;\
	else\
	  make do_export;\
	fi

do_export:
	rm -rf $(TARNAME)
	mkdir $(TARNAME)
	for i in $(EXPORT_FILES); do\
	  ../../tools/syseg-export -f $$i $(TARNAME);\
	done
	for i in $(EXPORT_NEW_FILES); do\
	  ../../tools/syseg-newfile -c $(TARNAME)/$$i;\
	done
	make $(TARNAME)/Makefile
	echo "DOCM4_DIST=yes" > $(TARNAME)/.dist
	tar zcvf $(TARNAME).tar.gz $(TARNAME)


clean-export:
	rm -f $(TARNAME).tar.gz
	rm -rf $(TARNAME)

.PHONY: syseg-export export clean-export

## End of export rules.





# Update docm4 files.
#
# These rules are not relevant for the source-code examples in this directory.
# The are provided to automatically update docm4 files when their respective
# sources change. It won't have effect in an exported directory, though.

-include .dist

ifneq (yes,$(DOCM4_DIST))


docm4_deps = ../../tools/docm4.m4 ../../tools/bintools.m4

Makefile : Makefile.m4 $(docm4_deps) 
	@path=$$(pwd) ; dir=$${path##*/};\
	 make -C .. $$dir/Makefile;
	@echo "syseg>>: Makefile has changed: all targets may need to be rebuilt."
	@echo "Building" $$(test -z "$(MAKECMDGOALS)" && echo "the default target" || echo "$(MAKECMDGOALS)")
	@make -f Makefile $(MAKECMDGOALS)

docm4_supported_files = README 

$(docm4_supported_files): % : %.m4 $(docm4_deps)
	@path=$$(pwd) ; dir=$${path##*/}; make -C .. $$dir/$(*) 

updatem4: Makefile
#	@path=$$(pwd) ; dir=$${path##*/}; make -C .. $$(for i in $(docm4_supported_files); do test -f $$dir/$$i.m4 && echo "$$dir/$$i" ; done)
	@make $(docm4_supported_files)

endif

# End of update docm4 files.


