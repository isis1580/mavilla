// Accueil.js
import { StyleSheet, Text, View,Image,TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native'; // Importer useNavigation
import BandePub from './BandePub';
import SectionHeader from './SectionHeader';
import { ScrollView } from 'react-native-gesture-handler';
import BandeMaisons from './BandeMaisons';
import BandeHotels from './BandeHotels';
import BandeParcelle from './BandeParcelle';
import HeaderScreen from './HeaderScreen';


const Accueil = () => {
  const navigation = useNavigation();
  const handlePress = () => {
    navigation.navigate('Maison'); 
  };
  

  return (
 
    <View style={styles.container}>
      <ScrollView style={styles.scrollcontainer}
        showsVerticalScrollIndicator={false}>
        <HeaderScreen/> 

        <View style={styles.Bandecontainer}>
          <SectionHeader 
            title={"Categories Maisons"} 
            buttonTitle={"Voir Tout"} 
            onPress={handlePress}
          />
          <BandeMaisons/>
        </View>
        <View style={styles.Bandecontainer}>
          
          <BandePub />
        </View>

        
        <View style={styles.Bandecontainer}>
          <BandeHotels />
        </View>
          
        <View style={styles.Bandecontainer}>
          <BandeParcelle />

        </View>

      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,

  },

  Bandecontainer:{
    marginTop:10,
    marginBottom:40
  }
});

export default Accueil;