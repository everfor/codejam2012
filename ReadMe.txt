Team:				RuntimeException (RTE for short)
Members:			Guang Yang(Alan Yang)
				Nguyen Knoi Tran

How to run the program?

1. Go to the terminal, type "python codejam2012/GUI/rte.py" to run the program.

2. Type the IP address, port for Feed-In process, and port for Trade booking/Confirmation process into the right text field    accoring to the labels before the text fields.

3. Click "Connect" button. That will create a connection with the server thourgh TCP/IP.

4. The Gant Chart for scheduling will show up. The scheduling of the program is just the same.

5. Click "Start" to start the feed in process.

6. The four areas on the right shows the real-time graph for the four strategies. The legend for the graphs are on the    bottom left part of the program.

7. The trade booking process runs in the same time.

8. Once it is completed, the "Send Report" button will be functional. Meanwhile a file called "history.txt" will be    automatically opened; it contains all the transaction histories in a tabular form.(If "history.txt" is empty upon opened, open it again and it will show eveything. Path: home/codejam2012/GUI)

9. Click "Send Report" to send the report. The ceremony ID will be displayed in the textfield previously named "Ceremony    ID".

10. To access the local json file storing all the data, go to home/codejam2012/GUI/Result.json; it is where all is stored.