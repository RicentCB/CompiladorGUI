library ieee;
use ieee.std_logic_1164.all;

entity ent is
  port (
    DATAIN
  ) ;
end ent ;
begin
    PBS : PROCESS(DATAIN, SHIFT)
    VARIABLE SHIFT_DATA : STD_LOGIC_VECTOR(7 DOWNTO 0);
    VARIABLE INDICE: INTEGER RANGE -4 TO 7;
    begin
        SHIFT_DATA := DATA_IN;
        FOR I IN 0 TO 2 LOOP
            FOR J IN 7 DOWNTO 0 LOOP
                IF SHIFT(I) = '1' THEN
                    INDICE := J - 2**I;
                    IF( INDICE < 0) THEN
                        SHIFT_DATA(J) := '0';
                    ELSE
                        SHIFT (J) :=SHIFT_DATA(INDICE);
                    END IF;
            END LOOP;
        END LOOP;
        DATAOUT <= SHIFT_DATA;
    END PROCESS PBS;

end PROGRAMA; 
    