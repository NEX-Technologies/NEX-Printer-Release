void setup() 
{
  Serial.begin(115200);
}

void loop() 
{
  if(Serial.available())
  {
    String data = Serial.readStringUntil("\n");
    data = data.substring(0, data.length() - 2);

    //Serial.print("Received: ");
    //Serial.println(data);

    if(data == "led_on")
    {
      digitalWrite(13, HIGH);

      Serial.println("DONE");
    }
    else if(data == "led_off")
    {
      digitalWrite(13, LOW);
    }
    
  }
  delay(1000);
}
