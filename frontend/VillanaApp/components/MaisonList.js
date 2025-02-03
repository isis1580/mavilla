import React, { useEffect, useState } from 'react';
import { View, Text, Image, TouchableOpacity, FlatList, Alert, SafeAreaView, StyleSheet } from 'react-native';
import axios from 'axios';
import { createMaterialTopTabNavigator } from '@react-navigation/material-top-tabs';
import { FontAwesome } from '@expo/vector-icons';
import { Actionsheet, Box } from 'native-base';
import { Video } from 'expo-av';
import AppBar from './AppBar';
import * as Sharing from 'expo-sharing'; // Pour partager des liens ou du texte

const serverIp = '10.125.9.182:8000';
const Tab = createMaterialTopTabNavigator();

const MaisonList = ({ navigation }) => {
  const [maisons, setMaisons] = useState([]);
  const [userImage, setUserImage] = useState('https://example.com/user.jpg');
  const [favorites, setFavorites] = useState(new Set());
  const [likes, setLikes] = useState(new Set());
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const maisonsResponse = await axios.get(`http://${serverIp}/maisons/`);
        const maisonsData = maisonsResponse.data.map(maison => ({
          ...maison,
          media: [
            ...maison.photos.map(photo => ({ ...photo, type: 'photo' })),
            ...maison.videos.map(video => ({ ...video, type: 'video' }))
          ]
        }));
        console.log("Données des maisons:", maisonsData); // Log des données
        setMaisons(maisonsData);
      } catch (error) {
        console.error('Erreur lors du fetch:', error);
      }
    };

    fetchData();
  }, []);

  const toggleFavorite = (maisonId) => {
    setFavorites((prevFavorites) => ({
      ...prevFavorites,
      [maisonId]: !prevFavorites[maisonId],
    }));
  };

  const toggleLike = (maisonId) => {
    setLikes((prevLikes) => ({
      ...prevLikes,
      [maisonId]: !prevLikes[maisonId],
    }));
  };


    // Fonction pour partager le lien via différentes plateformes
    const handleShare = (platform) => {
      const message = 'Check out this amazing property!'; // Message à partager
      const url = 'https://www.example.com'; // Lien à partager
  
      switch (platform) {
        case 'facebook':
          // Partage sur Facebook (peut être implémenté via une bibliothèque de partage ou Facebook SDK)
          Alert.alert('Partager sur Facebook');
          break;
        case 'whatsapp':
          // Partage sur WhatsApp (via URL scheme ou une bibliothèque dédiée)
          Alert.alert('Partager sur WhatsApp');
          break;
        case 'instagram':
          // Partage sur Instagram (via URL scheme ou une bibliothèque dédiée)
          Alert.alert('Partager sur Instagram');
          break;
        default:
          break;
      }
    };

  const showMaisonDetails = (maison) => {
    Alert.alert(
      'Détails de la maison',
      `Type: ${maison.type_maison}\nPrix: ${maison.prix}€\nChambres: ${maison.nombre_chambres}\nSalles de bain: ${maison.nombre_salles_de_bain}\nSalons: ${maison.nombre_salon}\nDescription: ${maison.description}`
    );
  };

  const RenderMaisonMemo = React.memo(({ item }) => (
    <View style={styles.maisonContainer}>
      
      <View style={styles.profilContainer}>
        <View style={styles.profilContainer1}>
          <TouchableOpacity style={styles.profilButton} onPress={() => navigation.navigate("Menu")}>
            <Image source={require('../assets/profil.jpg')} style={styles.userImage} />
           
          </TouchableOpacity>
          <Text style={styles.title}>Nom de l'utilisateur</Text>
        </View>
        <TouchableOpacity style={styles.rightIcon} onPress={() => toggleFavorite(item.id)}>
          <FontAwesome name={favorites[item.id] ? "bookmark" : "bookmark-o"} size={27} color={favorites[item.id] ? "#444" : "#052c65"} />
        </TouchableOpacity>
      </View>
      <Text style={styles.maisoninfo}>{item.type_maison} {item.prix} fCfa</Text>
      <View style={styles.container}>
        <FlatList
          data={item.media}
          keyExtractor={(mediaItem, index) => index.toString()}
          horizontal
          showsHorizontalScrollIndicator={false}
          renderItem={({ item }) => {
            if (item.type === 'photo') {
              return (
                <View style={styles.imageContainer}>
                  <Image 
                  source={{ uri: `${item.photos}`
                  
                 }} 
                  style={styles.image} />
                </View>
              );
            } else if (item.type === 'video') {
              return (
                <View style={styles.videoContainer}>
                  <Video
                    source={{ uri: `${item.video}` }}
                    style={styles.video}
                    resizeMode="contain"
                    shouldPlay={false}
                    isLooping
                  />
                </View>
              );
            }
          }}
        />
         {/* Icône de flèche droite */}
      <TouchableOpacity style={styles.arrowIconContainer}>
        <FontAwesome name="chevron-right" size={24} color="#052c65" />
      </TouchableOpacity>
        <View style={styles.absolutedetail}>
          <TouchableOpacity onPress={() => showMaisonDetails(item)} style={styles.detailsButton}>
            <Text style={styles.detail}>Voir Détails</Text>
          </TouchableOpacity>
        </View>
      </View>
      <View style={styles.iconsContainer}>
        <View style={styles.leftIcons}>
          <TouchableOpacity style={styles.leftIcon} onPress={() => toggleLike(item.id)}>
            <FontAwesome name={likes[item.id] ? "heart" : "heart-o"} size={27} color={likes[item.id] ? "red" : "#052c65"} />
          </TouchableOpacity>
           {/* Bouton de partage */}
        <TouchableOpacity style={styles.leftIcon} onPress={() => setIsOpen(true)}>
          <FontAwesome name="share-alt" size={27} color="#052c65" />
        </TouchableOpacity>
        </View>
        <TouchableOpacity onPress={() => showMaisonDetails(item)} style={styles.contactButton}>
          <Text style={styles.detailsButtonText}>Contacter</Text>
        </TouchableOpacity>
      </View>
      {/* Actionsheet pour partager */}
      <Actionsheet isOpen={isOpen} onClose={() => setIsOpen(false)}>
        <Actionsheet.Content>
          <Box w="100%" h={60} px={4} justifyContent="center">
            <Text fontSize="16" color="gray.500">Partager via</Text>
          </Box>
          <Actionsheet.Item onPress={() => handleShare('facebook')}>Partager sur Facebook</Actionsheet.Item>
          <Actionsheet.Item onPress={() => handleShare('whatsapp')}>Partager sur WhatsApp</Actionsheet.Item>
          <Actionsheet.Item onPress={() => handleShare('instagram')}>Partager sur Instagram</Actionsheet.Item>
          <Actionsheet.Item onPress={() => setIsOpen(false)}>Annuler</Actionsheet.Item>
        </Actionsheet.Content>
      </Actionsheet>

      
    </View>
  ));

  const AllMaisonsTab = () => (
    <FlatList
      data={maisons}
      keyExtractor={item => item.id.toString()}
      renderItem={({ item }) => (
        <RenderMaisonMemo key={item.id} item={item} />
      )}
      contentContainerStyle={styles.BlogContainer}
      
    />
  );

  const A_VendreTab = () => {
    const maisonsAVendre = maisons.filter(maison => maison.type_maison === 'vente');
    return (
      <FlatList
        data={maisonsAVendre}
        keyExtractor={item => item.id.toString()}
        renderItem={({ item }) => (
          <RenderMaisonMemo key={item.id} item={item} />
        )}
        contentContainerStyle={styles.BlogContainer}
        
      />
    );
  };

  const A_LouerTab = () => {
    const maisonsALouer = maisons.filter(maison => maison.type_maison === 'location');
    return (
      <FlatList
        data={maisonsALouer}
        keyExtractor={item => item.id.toString()}
        renderItem={({ item }) => (
          <RenderMaisonMemo key={item.id} item={item} />
        )}
        contentContainerStyle={styles.BlogContainer}
        
      />
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <AppBar />
      <View style={styles.TopContainer}>
        <View style={styles.TopContainer1}>
          <Text style={styles.toptext}>Catégorie Maison</Text>
          <Image source={require('../assets/niger.png')} style={styles.stateImage}
            />
        </View>

        <View style={styles.TopContainer2}>
          <TouchableOpacity style={styles.foricons} onPress={() => navigation.navigate('Search')}>
            <FontAwesome name="search" size={24} color="black" />
          </TouchableOpacity>
          <Image source={require('../assets/profil.jpg')} style={styles.foricons}
            />
        </View>
      </View>

      <Tab.Navigator>
        <Tab.Screen name="Tout" component={AllMaisonsTab} />
        <Tab.Screen name="À vendre" component={A_VendreTab} />
        <Tab.Screen name="À louer" component={A_LouerTab} />
      </Tab.Navigator>
    </SafeAreaView>
  );
};


const styles = StyleSheet.create({
container: {
  flex: 1,
},
maisonContainer: {
  backgroundColor: "#fff",
  marginBottom: 10,
},
TopContainer: {
  justifyContent: 'space-between',
  alignItems: 'center',
  flexDirection: 'row',
  paddingHorizontal: 10,
  marginVertical: 10,
},
TopContainer1: {
  flexDirection: 'row',
  alignItems: 'center',
  justifyContent: 'center',
},
absolutedetail: {
  flexDirection: 'row',
  position: 'absolute',
  margin: 20,
  left: -15,
  bottom: 0,
  borderRadius: 20,
  paddingHorizontal: 10,
},
detail: {
  fontSize: 15,
  color: '#fff'
},
BlogContainer: {},
toptext: {
  fontSize: 23,
  fontWeight: 'bold',
  color: '#444',
  marginLeft:30
},
TopContainer2: {
  flexDirection: 'row',
  alignItems: 'center',
  justifyContent: 'center',
},
image: {
  width: 350,
  height: 500,
  resizeMode: 'cover',
  margin: 5,
  borderRadius: 5,
},
video: {
  width: '350',
  height: 500, // Ajustez la hauteur selon vos besoins
},
iconsContainer: {
  flexDirection: 'row',
  justifyContent: 'space-between',
  alignItems: 'center',
  marginVertical: 15,
  paddingHorizontal:20,
},
leftIcons: {
  flexDirection: 'row',
  justifyContent: 'flex-start',
  alignItems: 'center',
  marginLeft: 10,
},
leftIcon: {
  marginRight:20,
},
rightIcon: {
  marginRight: 20,
},
profilContainer: {
  justifyContent: "space-between",
  flexDirection: 'row',
  alignItems: 'center'
},
profilContainer1: {
  flexDirection: 'row',
  alignItems: 'center',
  justifyContent: 'center',
  margin: 10,
},
profilButton: {
  justifyContent: 'center',
  alignItems: 'center',
},
userImage: {
  width: 40,
  height: 40,
  borderRadius: 50,
  backgroundColor: '#444',
  borderWidth: 2,
  marginRight: 5,
  borderColor: '#FFF',
  alignItems: 'center',
  justifyContent: 'center',
},
foricons: {
  width: 40,
  height: 40,
  borderRadius: 50,
  backgroundColor: '#fff',
  borderWidth: 2,
  marginRight: 5,
  borderColor: '#FFF',
  alignItems: 'center',
  justifyContent: 'center',
},
arrowIconContainer: {
  position: 'absolute',
  right: 10, // Ajustez la position selon vos besoins
  top: '50%', // Centré verticalement
  transform: [{ translateY: -12 }], // Ajustez pour centrer l'icône
  height:30,
  width:30,
  borderRadius:50,
  backgroundColor:'#fff',
  alignItems:'center',
  justifyContent:'center'
},
stateImage: {
  width: 20,
  height: 20,
  borderRadius: 50,
  resizeMode:'cover',
  borderWidth: 2,
  borderColor: '#FFF',
  alignItems: 'center',
  justifyContent: 'center',
},
detailsButton: {
  backgroundColor: '#052c65',
  borderRadius: 15,
  padding: 10,
},
contactButton:{
  justifyContent: 'center',
  alignItems: 'center',
  backgroundColor:'green',
  borderRadius: 10
},

detailsButtonText: {
  color: '#fff',
  textAlign: 'center',
  fontSize: 20,
  padding: 5
},
maisoninfo: {
  fontSize: 16,
  margin: 10,
},
});

export default MaisonList;