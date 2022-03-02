//import the required libraries
import processing.serial.*;

Serial mySerial;
Table table;
String filename;

void setup()
{
  //set mySerial to listen on COM port 10 at 9600 baud
  mySerial = new Serial(this, "COM11", 115200);
  
  table = new Table();
  //add a column header "Data" for the collected data
  table.addColumn("Data");
  //add a column header "Time" and "Date" for a timestamp to each data entry
  table.addColumn("Time");
  table.addColumn("Date");
}

void draw()
{
  //variables called each time a new data entry is received
  int d = day();
  int m = month();
  int y = year();
  int h = hour();
  int min = minute();
  int s = second();
  int ms = millis();
  String ms_str;
  int start = 0;
  int pos;
  String v;
  
  if (ms < 10)
  {
    ms_str = "00" + str(ms);
  }
  else if(ms < 100)
  {
    ms_str = "0" + str(ms);
  }
  else
  {
    ms_str = str(ms);
  }
  
  if(mySerial.available() > 0)
  {
    //set the value recieved as a String
    String value = mySerial.readString();
    //check to make sure there is a value
    if(value != null)
    {
      pos = value.indexOf('\r', start);
      while(pos != -1)
      {
        v = value.substring(start, pos);
        //add a new row for each value
        TableRow newRow = table.addRow();
        //place the new row and value under the "Data" column
        newRow.setString("Data", v);
        //place the new row and time under the "Time" column
        newRow.setString("Time", str(h) + ":" + str(min) + ":" + str(s) + "." + ms_str);
        //place the new row and date under the "Date" column
        newRow.setString("Date", str(d) + "/" + str(m) + "/" + str(y));
        start = pos + 2;
        pos = value.indexOf('\r', start);
      }
    }
  }
}

void keyPressed()
{
  //variables used for the filename timestamp
  int d = day();
  int m = month();
  int h = hour();
  int min = minute();
  int s = second();
  //variable as string under the data folder set as (mm-dd--hh-min-s.csv)
  filename = "data/" + str(m) + "-" + str(d) + "--" + str(h) + "-" + str(min) + "-" + str(s) + ".csv";
  //save as a table in csv format(data/table - data folder name table)
  saveTable(table, filename);
  exit();
}
