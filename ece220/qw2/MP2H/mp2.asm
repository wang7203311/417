	.ORIG	x3000
; this program translate the event list starting at x5000 in memory into the schedule at x4000
;then print out the schedule from the address x4000 to 404F
;register table
;R0: R0 is a temporary register
;R1: R1 contain the slot number number and address of the string. sometimes behave as temporary register
;R2: R2 behave like column counter. sometimes behave as temporary register
;R3: R3 contain the value of day and some times behave as temporary register
;R4: R4 contain the value of slot number and sometimes behave as temporary register
;R5: R5 contain the address of string and sometimes behave as temporary register
;R6: R6 contain the address after x5000 and sometimes behave as a temporary register 
;Initialization: initialize the schedule in memory locations x4000 through x404F
	LD R0, FOURK		; load the value x4000 to R0
	LD R3, EIGHTY		; load the value #80 to R3
	LD R4, LING		; load the value #0 to R4
INITIA	STR R4, R0, #0		; store the value #0 to the memmory address contained in R0
	ADD R0, R0, #1		; increment R1 by 1
	ADD R3, R3, #-1		; decrement R3 by 1
	BRp INITIA		; branch to INITIA if the value of R3 is positive
;transition
;extract data from x5000 to x4000
	LD R5, FIVEK		; load the value x5000 to R5
	ADD R6, R5, #0		; load the value of R5 to R6
	ADD R6, R6, #-1		; decrement R6 by 1
TRANS	ADD R6, R6, #1		; increment R6 by 1
	LDR R4, R6, #0		; load the value whoes address contained in R6 to R4
	BRnp TRANS		; branch to TRANS if the value of R4 is negative or positive
	ADD R6, R6, #1		; increment R6 by 1
	LDR R3, R6, #0		; load the value whoes address contained in R6 to R3 (day)
	ADD R6, R6, #1		; increment R6 by 1
	LDR R4, R6, #0		; load the value whoes address contained in R6 to R4 (slot number)
;check if in the range of slot number
	ADD R0, R4, #-15 	; substract R4 by 15 and store in R0 
	BRp WRONG_SLOT		; branch to WRONG_SLOT if the value of R0 is positive
	ADD R0, R4, #0		; increment R4 by 1 and store in R0
	BRn WRONG_SLOT		; branch to WRONG_SLOT if the value of R0 is positive	
	ST R1, R1_TRAN		; Store the value R1 in R1_TRAN
	ST R2, R2_TRAN		; Store the value R2 in R2_TRAN
	ST R5, R5_TRAN		; Store the value R3 in R3_TRAN
	AND R1, R1, #0		; clear R1
	ADD R1, R1, #1		; increment R1 by 1
	AND R5, R5, #0		; clear R5
	LD R0, FIVE		; load value #5 to R0, behave as a counter
LOOP_M	ADD R5, R5, #1		; increment R5 by 1 (R5 contain the day right now, 1 for Mon and 5 for Fri)
	ST R5, R5_LOOP		; Store the value R5 to R5_LOOP
	AND R2, R1, R3		; AND R1 with R3 and store in R2	
	BRp Mapping		; branch to Mapping if the value of the value of R2 is positive
DONE_MAP
	ADD R1, R1, R1		; left shift R1	
	LD R5, R5_LOOP		; load the value of R5_LOOP to R5
	ADD R0, R0, #-1		; decrement R0 by 1
	BRp LOOP_M		; branch to LOOP_M if R0 is positive
;RECOVER data
	LD R1, R1_TRAN		; load the value of R1_TRAN to R1
	LD R2, R2_TRAN		; load the value of R2_TRAN to R2
	ADD R5, R6, #1		; increment R6 by 1 and store in R5
	LDR R0, R6, #1		; load the value in address R6 + 1 to R0
	BRz EXTRA		; branch to DONE_TRANS if the value of R0 is zero
	BRnzp TRANS 		; branch to TRANS
Mapping
	ST R6, R6_MAP		; store the value of R6 in R6_MAP
	ST R1, R1_MAP		; store the value of R1 in R1_MAP
	ST R2, R2_MAP		; store the value of R2 in R2_MAP
	ST R0, R0_MAP		; store the value of R0 in R0_MAP
	LD R1, FIVE		; load the value #5 to R1
	LD R0, FOURK		; load the value x4000 to R0
	AND R6, R6, #0		; clear R6
MULTI	ADD R6, R6, R4		; add R4 with R6 and store in R6
	ADD R1, R1, #-1		; decrement R1 by 1
	BRnp MULTI		; branch to MULTI if the value of R1 is positive
	ADD R6, R5, R6		; add R5 and R6, store in R6(R5 contain the day right now, 1 for Mon and 5 for Fri)
	ADD R6, R6, #-1		; decrement R6 by 1
	ADD R2, R0, R6		; add R0 with R6 and store in R2
	LD R5, R5_TRAN		; load the value of R5_TRAN to R5
	LDR R0, R2, #0		; load the value in address R2 to R0
	ADD R0, R0, #0		; check the sign of the value R0
	BRnp CONFLICT		; branch to CONFLICT if is not zero(means alread have value here)
	STR R5, R2, #0		; store the value of R5 to the address contained in R2
	LD R6, R6_MAP		; load the value from R6_MAP to R6
	LD R1, R1_MAP		; load the value from R1_MAP to R1
	LD R2, R2_MAP		; load the value from R2_MAP to R2
	LD R0, R0_MAP		; load the value from R0_MAP to R0
	BRnzp DONE_MAP		; branch to DONE_MAP
EXTRA
;clear base
	LD R6, BASE
	AND R0, R0, #0
	STR R0, R6, #0			;clear x6000
	LD R1, SIXK			; 6000
BACKTRACK_OR_NEXT
	ADD R2, R1,#0			; POINTER
	ADD R2, R2,#1 
	LDR R3, R2,#0			; DAY
	ADD R2, R2,#1
	LDR R5, R2,#0			; TIME AND R1 IS 5000
;calculate the slot number
	ST R6, R6_TIME
	ST R1, R1_TIME
	ST R2, R2_TIME
	LD R2, FIFTEEN
	AND R6, R6, #0
	ADD R6, R6, #1
	AND R4, R4, #0
TIME 	AND R1, R6, R5
	BRz  NO_CALL
	JSR SUB_CHECK
	ADD R0, R0, #0
	BRnp NEXT_EVENT
NO_CALL	ADD R4, R4, #1	
	ADD R6, R6, R6
	ADD R2, R2, #-1
	BRp TIME
	LD R6, R6_TIME
	LD R1, R1_TIME
	LD R2, R2_TIME
;POP and backtrack
	LDR R0, R6, #0
	ADD R0, R0, #0
	BRz NOT_COMP		;check base
	ADD R6, R6, #1
	ADD R1, R2, #-5	
	BRnzp BACKTRACK_OR_NEXT
NEXT_EVENT
	NOT R6, R6
	ADD R6, R6, #1
	ADD R5, R5, R6
	LD R2, R2_TIME
	STR R5, R2, #0
	LD R6, R6_TIME
	LD R1, R1_TIME	
;push event
	ADD R6, R6, #-1	
	STR R1, R6, #0

	ADD R2, R2, #1
	ADD R1, R2, #0
	LDR R0, R2, #0
	ADD R0, R0, #0
	BRz DONE_STACK	
	BRnzp BACKTRACK_OR_NEXT	
DONE_STACK
	LD R1, SIXK
NEXT_E	ADD R2, R1, #0
	ADD R2, R2, #1
	LDR R3, R2, #0
	ADD R2, R2, #1
	LDR R4, R2, #0
	JSR SUB_STORE
	ADD R1, R2, #1
	LDR R0, R1, #0
	ADD R0, R0, #0
	BRnp NEXT_E

R1_TRAN	.BLKW	#1
R2_TRAN	.BLKW	#1
R5_TRAN	.BLKW	#1
R6_MAP	.BLKW	#1
R1_MAP	.BLKW	#1
R2_MAP	.BLKW	#1
R0_MAP	.BLKW	#1
R1_PRINT.BLKW	#1
R5_LOOP	.BLKW	#1
R6_TIME	.BLKW	#1
R1_TIME	.BLKW	#1
R2_TIME .BLKW	#1
V_LINE	.FILL	x7C
N_LINE	.FILL	xA	
FIVE	.FILL	#5	
LING	.FILL	X0000
EIGHTY	.FILL	#80	
FOURK 	.FILL	x4000
FIVEK	.FILL	x5000
SIXK	.FILL	x6000
BASE	.FILL	x8000
FIFTEEN	.FILL	#15



DONE_TRANS
	LEA R1, NUL		; load the address NUL to R1
	JSR PRINT_CENTERED	; call subroutine to print the day
	LD R0, V_LINE		; load the value of ASCII "|" to R0
	OUT			; print out "|"
	LEA R1, MON		; load the address MON to R1
	JSR PRINT_CENTERED	; call subroutine to print the day
	LD R0, V_LINE		; load the value of ASCII "|" to R0
	OUT			; print out "|"
	LEA R1, THU		; load the address THU to R1
	JSR PRINT_CENTERED	; call subroutine to print the day
	LD R0, V_LINE		; load the value of ASCII "|" to R0
	OUT			; print out "|"
	LEA R1, WED		; load the address WED to R1
	JSR PRINT_CENTERED	; call subroutine to print the day
	LD R0, V_LINE		; load the value of ASCII "|" to R0
	OUT			; print out "|"
	LEA R1, THU		; load the address THU to R1
	JSR PRINT_CENTERED	; call subroutine to print the day
	LD R0, V_LINE		; load the value of ASCII "|" to R0
	OUT			; print out "|"
	LEA R1, FRI		; load the address FRI to R1
	JSR PRINT_CENTERED	; call subroutine to print the day
	LD R0, N_LINE		; load the value of ASCII newline to R0
	OUT			; print out newline
;print schedule
	AND R1, R1, #0		; clear R1, behave like row counter
	LD R3, FOURK		; load the value x4000 to R3
;check row
DONE_COL	
	LD R2, FIVE		; load the value #5 to R2, behave like column counter
	ADD R0, R1, #-15	; decrement R1 by 15 and store in R0
	BRp DONE		; branch DONE if R0 is DONE
	JSR PRINT_SLOT		; call subroutine to ptint time
	ST R1, R1_PRINT		; store R1 in R1_PRINT
COLUMN	LD R0, V_LINE		; load the value of ASCII "|" to R0
	OUT			; print out "|"
	LDR R4, R3, #0		; load the value contained in address R3 to R4
	BRnp PT			; branch to PT if R4 is negative or positive
	LEA R1, NUL		; load the address NUL to R1
	JSR PRINT_CENTERED	; call subroutine to print string
	BRnzp DONE_NU		; branch to DONE_NU
PT	LDR R1, R3, #0		; load the value contained in the address R3 to R1
	JSR PRINT_CENTERED	; call subroutine to print string
DONE_NU	ADD R3, R3, #1		; increment R3 by 1
	ADD R2, R2, #-1		; decrement R2 by 1
	BRp COLUMN		; branch to COLUMN if R2 is positive
	LD R1, R1_PRINT		; load the from R1_PRINT to R1
	LD R0, N_LINE		; load the value of newline to R0
	OUT			; print out new line
	ADD R1, R1, #1		; increment R1 by 1
	BRnzp DONE_COL		; branch to DONE_COL
;CONFLICT PART			
CONFLICT
	ADD R0, R5, #0		; add R5 to R0
	PUTS			; print the string
	LEA R0,CONF		;load the address CONF to R0
	PUTS			; print the string
	BRnzp DONE		; branch to DONE
WRONG_SLOT
	ADD R0, R5, #0		; add R5 to R0
	PUTS			; print string
	LEA R0, WRONG		; load the address WRONG to R0
	PUTS			; print the string
	BRnzp DONE		; branch to DONE
NOT_COMP
	LEA R0,FAIL
	PUTS
	BRnzp DONE
DONE	HALT			; halt			
NUL	.STRINGZ ""
MON	.STRINGZ "Mon"
TUE	.STRINGZ "Tue"
WED	.STRINGZ "Wed"
THU	.STRINGZ "Thu"
FRI	.STRINGZ "Fri"
CONF	.STRINGZ " conflicts with an earlier event.\n"
WRONG	.STRINGZ " has an invalid slot number.\n"
FAIL	.STRINGZ "Could not fit all events into schedule.\n"


;SUBROUTINE
PRINT_SLOT
;save the register
	ST R0, SV_R0		;store the value of R0 to SV_R0	
	ST R1, SV_R1		;store the value of R1 to SV_R1
	ST R2, SV_R2		;store the value of R2 to SV_R2
	ST R7, SV_R7		;store the value of R7 to SV_R7
;check out whether the value of R1 is less than 2	
	ADD R2,R1,#-2		;subtract R1 by 2 and store in R2
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



SUB_CHECK; check mapping
;FILL R1 = #1, R0 = 5, 		
	ST R1, R1_SUB		; Store the value R1 in R1_TRAN
	ST R2, R2_SUB		; Store the value R2 in R2_TRAN
	ST R5, R5_SUB		; Store the value R3 in R3_TRAN
	ST R7, R7_SUB
	AND R1, R1, #0		; clear R1
	ADD R1, R1, #1		; increment R1 by 1
	AND R5, R5, #0		; clear R5
	LD R0, FIVE_SUB		; load value #5 to R0, behave as a counter
LOOP_SUB
	ADD R5, R5, #1		; increment R5 by 1 (R5 contain the day right now, 1 for Mon and 5 for Fri)
	ST R5, R5_LOOP_S	; Store the value R5 to R5_LOOP
	AND R2, R1, R3		; AND R1 with R3 and store in R2	
	BRp Mapping_SUB		; branch to Mapping if the value of the value of R2 is positive
DONE_MAP_SUB
	ADD R1, R1, R1		; left shift R1	
	LD R5, R5_LOOP_S	; load the value of R5_LOOP to R5
	ADD R0, R0, #-1		; decrement R0 by 1
	BRp LOOP_SUB		; branch to LOOP_M if R0 is positive
	BRnzp DONE_SUB
;Mapping alorithm:the address in schedule is 4000+slot number*5+day-1
Mapping_SUB
	ST R6, R6_MAP_S		; store the value of R6 in R6_MAP
	ST R1, R1_MAP_S		; store the value of R1 in R1_MAP
	ST R2, R2_MAP_S		; store the value of R2 in R2_MAP
	ST R0, R0_MAP_S		; store the value of R0 in R0_MAP
	LD R1, FIVE_SUB		; load the value #5 to R1
	LD R0, FOUR_SUB		; load the value x4000 to R0
	AND R6, R6, #0		; clear R6
MULTI_SUB
	ADD R6, R6, R4		; add R4 with R6 and store in R6  (R4 is slot number)
	ADD R1, R1, #-1		; decrement R1 by 1
	BRnp MULTI_SUB		; branch to MULTI if the value of R1 is positive
	ADD R6, R5, R6		; add R5 and R6, store in R6(R5 contain the day right now, 1 for Mon and 5 for Fri)
	ADD R6, R6, #-1		; decrement R6 by 1
	ADD R2, R0, R6		; add R0 with R6 and store in R2
	LDR R0, R2, #0		; load the value in address R2 to R0
	ADD R0, R0, #0		; check the sign of the value R0
	BRnp FAIL_S		; branch to CONFLICT if is not zero(means alread have value here)
	LD R6, R6_MAP_S		; load the value from R6_MAP to R6
	LD R1, R1_MAP_S		; load the value from R1_MAP to R1
	LD R2, R2_MAP_S		; load the value from R2_MAP to R2
	LD R0, R0_MAP_S		; load the value from R0_MAP to R0
	BRnzp DONE_MAP_SUB	; branch to DONE_MAP
FAIL_S	AND R0, R0, #0
	BRnzp DONE_F
DONE_SUB
	AND R0, R0,#0
	ADD R0, R0,#1
	LD R1, R1_SUB		; load the value of R1_TRAN to R1
	LD R2, R2_SUB		; load the value of R2_TRAN to R2
	LD R5, R5_SUB
DONE_F	LD R7, R7_SUB
	RET

FIVE_SUB.FILL	x0005
FOUR_SUB.FILL	x4000
R1_SUB	.BLKW	#1
R2_SUB	.BLKW	#1
R5_SUB	.BLKW	#1
R7_SUB	.BLKW	#1
R6_MAP_S.BLKW	#1
R1_MAP_S.BLKW	#1
R2_MAP_S.BLKW	#1
R0_MAP_S.BLKW	#1
R5_ST	.BLKW	#1
R5_LOOP_S.BLKW	#1
SUB_STORE
	;store part
	ST R1, R1_SUB		; Store the value R1 in R1_TRAN
	ST R2, R2_SUB		; Store the value R2 in R2_TRAN
	ST R5, R5_SUB		; Store the value R3 in R3_TRAN
	ST R7, R7_SUB
	AND R1, R1, #0		; clear R1
	ADD R1, R1, #1		; increment R1 by 1
	AND R5, R5, #0		; clear R5
	LD R0, FIVE_SUB		; load value #5 to R0, behave as a counter
LOOP_ST
	ADD R5, R5, #1		; increment R5 by 1 (R5 contain the day right now, 1 for Mon and 5 for Fri)
	ST R5, R5_ST		; Store the value R5 to R5_LOOP
	AND R2, R1, R3		; AND R1 with R3 and store in R2	
	BRp Mapping_ST		; branch to Mapping if the value of the value of R2 is positive
DONE_MAP_ST
	ADD R1, R1, R1		; left shift R1	
	LD R5, R5_ST		; load the value of R5_LOOP to R5
	ADD R0, R0, #-1		; decrement R0 by 1
	BRp LOOP_ST		; branch to LOOP_M if R0 is positive
	BRnzp DONE_ST
;Mapping alorithm:the address in schedule is 4000+slot number*5+day-1
Mapping_ST
	ST R6, R6_MAP_S		; store the value of R6 in R6_MAP
	ST R1, R1_MAP_S		; store the value of R1 in R1_MAP
	ST R2, R2_MAP_S		; store the value of R2 in R2_MAP
	ST R0, R0_MAP_S		; store the value of R0 in R0_MAP
	LD R1, FIVE_SUB		; load the value #5 to R1
	LD R0, FOUR_SUB		; load the value x4000 to R0
	AND R6, R6, #0		; clear R6
MULTI_ST
	ADD R6, R6, R4		; add R4 with R6 and store in R6  (R4 is slot number)
	ADD R1, R1, #-1		; decrement R1 by 1
	BRnp MULTI_ST		; branch to MULTI if the value of R1 is positive
	ADD R6, R5, R6		; add R5 and R6, store in R6(R5 contain the day right now, 1 for Mon and 5 for Fri)
	ADD R6, R6, #-1		; decrement R6 by 1
	ADD R2, R0, R6		; add R0 with R6 and store in R2
	LD R1, R1_SUB
	STR R1, R2,#0
	LD R6, R6_MAP_S		; load the value from R6_MAP to R6
	LD R1, R1_MAP_S		; load the value from R1_MAP to R1
	LD R2, R2_MAP_S		; load the value from R2_MAP to R2
	LD R0, R0_MAP_S		; load the value from R0_MAP to R0
	BRnzp DONE_MAP_ST	; branch to DONE_MAP
DONE_ST
	LD R1, R1_SUB		; load the value of R1_TRAN to R1
	LD R2, R2_SUB		; load the value of R2_TRAN to R2
	LD R5, R5_SUB
	LD R7, R7_SUB
	RET
	.END
