 struct CommandReq
        {
            double Pos;
            double Velos;
            double Acc;
            uint8_t mode
            uint8_t ID
            double lambda
            double CMD
            
            /*
            char    sMark[6];//start flag\r\n*KW
            short   nPackLen ;//packet length
            short   nFlag ;//command ID 0x0002
            int nGisIp ;//GIS port
            short   nPort;//GIS Port
            char    sData[50];//command string
            char    sEnd[2];//end flag "\r\n" 
            */

        };
        //source code
        
        CommandReq stResq;
        memset(&stResq, 0, sizeof(stResq));
        sprintf(stResq.sMark,"\r\n%s","*KW");
        stResq.Pos = 0x0002;
        stResq.Velos = sizeof(stResq);
        stResq.Acc = 0;
        stResq.mode = 0;
        stResq.ID = 0;
        stResq.lambda = 0;
        stResq.CMD = 0;
        
        /*
        CommandReq stResq;
        memset(&stResq, 0, sizeof(stResq));
        sprintf(stResq.sMark,"\r\n%s","*KW");
        stResq.nFlag = 0x0002;
        stResq.nPackLen = sizeof(stResq);
        stResq.nGisIp = 0;
        stResq.nPort = 0;
        strcpy(stResq.sData,"*KW,CC09C00001,015,080756,#");
        strncpy(stResq.sEnd,"\r\n",2);
        */
