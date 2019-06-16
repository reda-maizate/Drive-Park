import React from 'react';
import {
  Container, Content, Text,View,StyleSheet
} from 'native-base';
import Spacer from './Spacer';
import MapView  from 'react-native-maps'


const About = () => (
  <View style={{position: 'absolute',
  top : 0,
  left : 0,
  bottom : 0,
  right : 0,}}>
    <MapView style={ {position: 'absolute',
    top : 0,
    left : 0,
    bottom : 0,
    right : 0,}}
    showsUserLocation={true}
    
    initialRegion={{
      latitude: 48.8753258,
      longitude:  2.4114326,
      latitudeDelta: 0.0922,
      longitudeDelta: 0.0421,
    } }>
    


<MapView.Marker
    coordinate={{
      latitude: 48.8753258,
      longitude:  2.4114326,
    }}
    title = {'Parking Paul Meurice'}
    description = {'Parking situé à la rue Paul Meurice'}/>
<MapView.Marker
    coordinate={{
      latitude: 48.8795475,
      longitude:  2.3964909,
    }}
    title = {'Parking des lilas'}
    description = {'Parking situé à la rue des lilas'}/>
<MapView.Marker
    coordinate={{
      latitude: 48.8769923,
      longitude:  2.3859792,
    }}
    title = {'Parking des solitaires'}
    description = {'Parking situé à la rue des soliataires'}/>
  </MapView>
    </View>
);





export default About;
