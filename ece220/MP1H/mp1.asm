	.ORIG x3000
	LD	R0,BITS
	ADD	R2,R0,#0
	ADD	R3,R0,#0
	ADD	R4,R0,#0
	ADD	R5,R0,#0
	ADD	R6,R0,#0

	; let's try PRINT_SLOT ... 11:00
	AND	R1,R1,#0
	ADD	R1,R1,#15

	; set a breakpoint here in the debugger, then use 'next' to
	; execute your subroutine and see what happens to the registers;
	; they're not supposed to change (except for R7)...
	
	JSR	PRINT_SLOT
	; we're short on human time to test your code, so we'll do 
	; something like the following instead (feel free to replicate)...
	LEA	R1, R0_BAD
	JSR	PRINT_CENTERED	
	LD	R7,BITS
	NOT	R7,R7
	ADD	R7,R7,#1
	ADD	R0,R0,R7
	BRz	R0_OK
	LEA	R0,R0_BAD
	PUTS
R0_OK	

	; this trap changes register values, so it's not sufficient
	; to check that all of the registers are unchanged; HALT may
	; also lead to confusion because the register values differ
	; for other reasons (R7 differences, for example).
	HALT

BITS	.FILL	xABCD	; something unusual
VLINE	.FILL	x7C	; ASCII vertical line character
R0_BAD	.STRINGZ "PRINT_SLOT changes R0!\n"
STRIN	.STRINGZ "F151"

;The subroutine must output exactly six characters to the display, including an appropriate 
;hour number (R1+7 as a two-digit number, possibly including a leading zero), a colon (:), 
;two zeroes, and a trailing space. 

;register table
;R0: used to print the ASCII value
;R1: store the value between 0 to 15
;R2: temporary register.
;R7: changed when use trap instruction and contain the address that subroutine should return.

PRINT_SLOT
;save the register
	ST R0, SV_R0		;store the value of R0 to SV_R0	
	ST R1, SV_R1		;store the value of R1 to SV_R1
	ST R2, SV_R2		;store the value of R2 to SV_R2
	ST R7, SV_R7		;store the value of R7 to SV_R7
;check out whether the value of R1 is less than 2	
	ADD R2,R1,-2		;subtract R1 by 2 and store in R2
	BRp MORE_THAN_TWO	;if R2 is positive, then move the MORE_THAN_TWO
	LD R0, ZERO		;load the value of ASCII '0' to R0
	OUT			;print out '0'
	LD R2, Z_TO_S		;load the value of difference between decimal '0' and ASCII '7' to R2
	ADD R0, R1, R2		;add R1 and R2 and store in R0
	OUT			;print out the ASCII value stored in R0
	LD R0, COLON		;load the value of ASCII ':' to R0
	OUT			;print out ':'
	LD R0, ZERO		;load the value of ASCII '0' to R0
	OUT			;print out '0'
	OUT			;print out '0'
	LD R0, SPACE		;load the value of ASCII ' ' to R0
	OUT			;print out ' '
	BRnzp RECOVER		;branch to RECOVER

;if the value of R1 is greater than 2
MORE_THAN_TWO
	ADD R2, R1,#-12		;subtract R1 by 12 and store in R2
	BRp MORE_THAN_XII 	;branch to MORE_THAN_XII if the value of R2 is positive
	LD R0, ONE		;load the value of ASCII '1' to R0		
	OUT			;print out '1'
	LD R2, T_TO_Z		;load the value of difference between decimal '3' and ASCII '0' to R2
	ADD R0, R1, R2		;add R1 and R2 and store in R0
	OUT			;print out the ASCII value stored in R0
	LD R0, COLON		;load the value of ASCII ':' to R0
	OUT			;print out ':'
	LD R0, ZERO		;load the value of ASCII '0' to R0
	OUT			;print out '0'
	OUT			;print out '0'
	LD R0, SPACE		;load the value of ASCII ' ' to R0
	OUT			;print out ' '
	BRnzp RECOVER		;branch to RECOVER
;if the value of R1 is greater than 12
MORE_THAN_XII
	LD R0, TWO		;load the value of ASCII '2' to R0	
	OUT			;print out '2'
	LD R2, O_TO_Z		;load the value of difference between decimal '13' and ASCII '0' to R2
	ADD R0, R1, R2		;add R1 and R2 to R0
	OUT			;print out the ASCII value stored in R0
	LD R0, COLON		;load the value of ASCII ':' to R0 
	OUT			;print out ':'
	LD R0, ZERO		;load the value of ASCII '0' to R0
	OUT			;print out '0'
	OUT			;print out '0'
	LD R0, SPACE		;load the value of ASCII ' ' to R0
	OUT			;print out ' '
RECOVER
	LD R0, SV_R0		;reload the initial value of R0
	LD R1, SV_R1		;reload the initial value of R1
	LD R2, SV_R2		;reload the initial value of R2
	LD R7, SV_R7		;reload the initial value of R7 
	RET			;return to the address contained by R7

SV_R0	.BLKW #1		;save R0
SV_R1	.BLKW #1		;save R1
SV_R2	.BLKW #1		;save R2
SV_R7	.BLKW #1		;save R7
ZERO	.FILL	x30		;the value of ASCII '0'
ONE	.FILL	x31		;the value of ASCII '1'
TWO	.FILL	x32		;the value of ASCII '2'
COLON	.FILL	x3A		;the value of ASCII ':'
Z_TO_S	.FILL	x37		;the value of difference between decimal '0' and ASCII '7'
T_TO_Z	.FILL	x2D		;the value of difference between decimal '3' and ASCII '0'
O_TO_Z	.FILL	x23		;the value of difference between decimal '13' and ASCII '0'
SPACE	.FILL	x20		;the value of ASCII ' '

;The subroutine must output exactly six characters to the display. For strings longer than 
;six characters, the first six characters should be displayed. For strings shorter than six 
;characters, leading and trailing spaces must be added to output six total characters. For 
;short, odd-length strings, use one more trailing space than leading space. 

;register table 
;R0: used to print ASCII value
;R1: store the address of the string
;R2: temporary register and left space counter
;R3: temporary register and contain the length of string
;R4: temporary register and right space counter
;R5: temporary register
;R7: changed when use trap instruction and contain the address that subroutine should return.

PRINT_CENTERED
;save register
	ST R0, SVR0_CT		;store the value of R0 to SVR0_CT
	ST R1, SVR1_CT		;store the value of R1 to SVR1_CT
	ST R2, SVR2_CT		;store the value of R2 to SVR2_CT
	ST R3, SVR3_CT		;store the value of R3 to SVR3_CT
	ST R4, SVR4_CT		;store the value of R4 to SVR4_CT
	ST R5, SVR5_CT		;store the value of R5 to SVR5_CT
	ST R7, SVR7_CT		;store the value of R7 to SVR7_CT
;check the length of the string
	AND R3,R3,#0		;clear R0
	ADD R2,R1,#0		;store R1 in R2
LOOP	LDR R5,R2,#0		;load the value from the memory contained in R2 to R5
	BRz DONE_LENGTH		;branch to DONE_LENGTH if R5 is zero
	ADD R2,R2,#1		;increment R2 by 1
	ADD R3,R3,#1		;increment R3 by 1
	ADD R4,R3,#-6		;substract R3 by 6 and store in R4
	BRp MORE_THAN_SIX	;branch to MORE_THAN_SIX if the value of R4 is positive
	BRnzp LOOP 		;branch to LOOP

;divide difference between 6-length of the string by 2	
DONE_LENGTH
	AND R2,R2,#0		;clear R2
	ADD R4,R3,#0		;store R3 to R4
	NOT R3,R3		;NOT R3
	ADD R3,R3,#1		;increment R3 by 1
	ADD R4,R3,#6		;add R3 and store the value in R4
DIVIDE	ADD R4,R4,#-2		;subtract R4 by 2
	BRn DONE_DIVIDE		;branch to DONE_DIVIDE
	ADD R2,R2,#1    	;increment the left space counter R2 by 1
	BRnzp DIVIDE		;branch to DIVIDE
;find the right space counter
DONE_DIVIDE
	NOT R4,R2		;NOT R2 and store in R4
	ADD R4,R4,#1		;increment R4 by 1
	ADD R4,R4,#6		;add R4 by 6
	ADD R4,R4,R3		;add the right space counter R4 and R3 and store in R4
	
;left space	
LEFT	ADD R2,R2,#-1		;decrement R2 by 1
	BRn PRINT_STRING	;branch to PRINT_STRING if R2 is negative
	LD  R0,SPACE_CT		;load the value of ASCII ' '		
	OUT			;print out ' '
	BRnzp	LEFT		;branch to LEFT
	
;print the string	
PRINT_STRING
	ADD R0,R1,#0		;store the value of R1
	PUTS			;print string
	BRnzp RIGHT_SPACE	;branch to RIGHT_SPACE
	
RIGHT_SPACE
RIGHT	ADD R4,R4,#-1		;decrement R4 by 1	
	BRn RECOVER_CT		;branch to RECOVER_CT if R4 is negative
	LD  R0,SPACE_CT		;load the value of ASCII ' '
	OUT			;print out ' '
	BRnzp RIGHT		;branch to RIGHT
;if the string is more than 6 characters	
MORE_THAN_SIX
	ADD R3,R3,#-1		;decrement R3 by 1
PRINT	LDR R0,R1,#0		;load the value from the memory contained in R1 to R0
	OUT			;print the value store in R0
	ADD R1,R1,#1		;increment R1 by 1
	ADD R3,R3,#-1		;decrement R3 by 1
	BRp PRINT		;branch to PRINT if R3 is positive
	BRnzp RECOVER_CT	;branch to RECOVER_CT
;reload the register 	
RECOVER_CT
	LD R0, SVR0_CT		;reload the initial value of R0
	LD R1, SVR1_CT		;reload the initial value of R1
	LD R2, SVR2_CT		;reload the initial value of R2
	LD R3, SVR3_CT		;reload the initial value of R3
	LD R4, SVR4_CT		;reload the initial value of R4
	LD R5, SVR5_CT		;reload the initial value of R5
	LD R7, SVR7_CT		;reload the initial value of R7
	RET			;return to the address contained by R7
		
SVR0_CT	.BLKW #1		;save R0
SVR1_CT	.BLKW #1		;save R1
SVR2_CT	.BLKW #1		;save R2
SVR3_CT	.BLKW #1		;save R3
SVR4_CT	.BLKW #1		;save R4
SVR5_CT	.BLKW #1		;save R5
SVR7_CT	.BLKW #1		;save R7
SPACE_CT.FILL	x20		;the value of ASCII ' '
	.END
