import { StyleSheet,View} from 'react-native'; 
import React from 'react'; 
import TitlesDetails from './TitlesDetails';
import ImageDetails from './ImageDetails';
import AppBar from './AppBar';
import { useNavigation } from '@react-navigation/native';



const HotelsDetails = ({ route }) => { 
  const navigation = useNavigation();
  const { trip } = route.params;
  console.log("Données de trip :", trip); // Ajoutez ce log 
  const slides = [trip.photos];
  const _goBack = () => {
    navigation.goBack(); 
  };

  return ( 
    <View style={styles.container}> 
      

      <ImageDetails slides={slides} />
      <AppBar />
      <TitlesDetails trip={trip}/>  
         
    </View>
  ); 
}


const styles = StyleSheet.create({ 
  container: {
    flex: 1,
    backgroundColor:'white'

  },
  

});

export default HotelsDetails;