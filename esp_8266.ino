#define STEPPER_PIN_1 05
#define STEPPER_PIN_2 04
#define STEPPER_PIN_3 00
#define STEPPER_PIN_4 02
int step_number = 0;
const int trig = 12;
const int echo = 13;
long lecture_echo;
long cm;


#include <ESP8266WiFi.h>
const char* ssid =  "FEVER";
const char* password = "fever95400@@";
WiFiServer server( 80 ); //Demarrage du serveur


void setup() {

/* ultrason */

  pinMode(trig, OUTPUT); 
  digitalWrite(trig, LOW); 
  pinMode(echo, INPUT); 
  Serial.begin(9600); 


/* MOTOR */



pinMode(STEPPER_PIN_1, OUTPUT);
pinMode(STEPPER_PIN_2, OUTPUT);
pinMode(STEPPER_PIN_3, OUTPUT);
pinMode(STEPPER_PIN_4, OUTPUT);

/**************/


 
Serial.begin(9600); // Ouverture du port serie
delay(10);
Serial.print("Connecting to "); //Wifi
Serial.println(ssid);
WiFi.begin(ssid, password); // On se connecte au réseau WiFi
while (WiFi.status() != WL_CONNECTED) {
delay(500);
Serial.print(".");
}
Serial.println("");
Serial.println("WiFi OK"); // connexion OK, on demarre le server
server.begin();
Serial.println("Server OK");
 
Serial.println(WiFi.localIP()); // On indique sur le port serie l'adresse ip
}



void loop() {
WiFiClient client = server.available();// intéroger lsereur s'il est dispo
if(!client){
return;
}
//Attente d’un client
Serial.println( "changement" );
while( !client.available() ){
delay( 10 );
}
 // Récupération de la première ligne de la requête
String request = client.readStringUntil( '\r' );
client.flush();
{
 
// LED CLASSIQUE
if ( request.indexOf( "up" ) != -1 )
 up() ;// souleve on

if ( request.indexOf( "down" ) != -1 )
 down(); // descend barriere 
if ( request.indexOf( "action" ) != -1 )
 action(); // action ( up / 5S / down )

 

}
{
// Page HTML
client.println( "HTTP/1.1 200 OK" );
client.println( "Content-Type: text/html" );
client.println(); //  Mandatory !
client.println( "<!DOCTYPE HTML>" );
client.println( "<html><body>DRIVEPARK <br></body>");
// LED VERT
client.println( "<a href=\"/up\"\"><button>UP BARRIERE</button></a><br>" );
client.println( "<a href=\"/down\"\"><button>DOWN BARRIERE</button></a><br>" );
client.println( "<a href=\"/action\"\"><button>ACTION</button></a><br>" );

// FIN PAGE HTML
client.println( "</html>" );
}
  digitalWrite(trig, HIGH); 
  delayMicroseconds(10); 
  digitalWrite(trig, LOW); 
  lecture_echo = pulseIn(echo, HIGH); 
  cm = lecture_echo / 58; 
  Serial.print("Distancem : "); 
  Serial.println(cm); 
  delay(200);


}
 
/******    MOUVEMENT MOTEUR      *******/


void up(){
   for(int a=0; a<500;a++){
  OneStep(false);
  delay(2);

 }
  delay(4000);
  }

void down(){
  

   for(int a=0; a<500;a++){
  OneStep(true);
  delay(2);

 }
  //delay(5000);
  }



void action(){
    up();
    digitalWrite(trig, HIGH); 
  delayMicroseconds(10); 
  digitalWrite(trig, LOW); 
  lecture_echo = pulseIn(echo, HIGH); 
  cm = lecture_echo / 58; 
 Serial.println(cm);
  while(cm <= 15)
  {
    delay(500);
    digitalWrite(trig, HIGH); 
  delayMicroseconds(10); 
  digitalWrite(trig, LOW); 
  lecture_echo = pulseIn(echo, HIGH); 
  cm = lecture_echo / 58; 
    Serial.println(cm+"a");
    
  }
  down(); 
}





void OneStep(bool dir){
    if(dir){
switch(step_number){
  
  case 0:
  digitalWrite(STEPPER_PIN_1, HIGH);
  digitalWrite(STEPPER_PIN_2, LOW);
  digitalWrite(STEPPER_PIN_3, LOW);
  digitalWrite(STEPPER_PIN_4, LOW);
  break;
  case 1:
  digitalWrite(STEPPER_PIN_1, LOW);
  digitalWrite(STEPPER_PIN_2, HIGH);
  digitalWrite(STEPPER_PIN_3, LOW);
  digitalWrite(STEPPER_PIN_4, LOW);
  break;
  case 2:
  digitalWrite(STEPPER_PIN_1, LOW);
  digitalWrite(STEPPER_PIN_2, LOW);
  digitalWrite(STEPPER_PIN_3, HIGH);
  digitalWrite(STEPPER_PIN_4, LOW);
  break;
  case 3:
  digitalWrite(STEPPER_PIN_1, LOW);
  digitalWrite(STEPPER_PIN_2, LOW);
  digitalWrite(STEPPER_PIN_3, LOW);
  digitalWrite(STEPPER_PIN_4, HIGH);
  break;

} 
  }else{
    switch(step_number){
  case 0:
  digitalWrite(STEPPER_PIN_1, LOW);
  digitalWrite(STEPPER_PIN_2, LOW);
  digitalWrite(STEPPER_PIN_3, LOW);
  digitalWrite(STEPPER_PIN_4, HIGH);
  break;
  case 1:
  digitalWrite(STEPPER_PIN_1, LOW);
  digitalWrite(STEPPER_PIN_2, LOW);
  digitalWrite(STEPPER_PIN_3, HIGH);
  digitalWrite(STEPPER_PIN_4, LOW);
  break;
  case 2:
  digitalWrite(STEPPER_PIN_1, LOW);
  digitalWrite(STEPPER_PIN_2, HIGH);
  digitalWrite(STEPPER_PIN_3, LOW);
  digitalWrite(STEPPER_PIN_4, LOW);
  break;
  case 3:
  digitalWrite(STEPPER_PIN_1, HIGH);
  digitalWrite(STEPPER_PIN_2, LOW);
  digitalWrite(STEPPER_PIN_3, LOW);
  digitalWrite(STEPPER_PIN_4, LOW);
 
  
} 
  }
step_number++;
  if(step_number > 3){
    step_number = 0;
  }
}



  
