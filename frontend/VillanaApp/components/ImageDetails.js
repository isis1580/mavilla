import { FlatList, StyleSheet, Text, View, Image } from 'react-native';
import React from 'react';
import { useNavigation } from '@react-navigation/native';


const ImageDetails = ({ slides }) => {
    const navigation = useNavigation();
    

    const flatSlides = slides && Array.isArray(slides[0]) ? slides[0] : [];

    console.log("Données plates pour le rendu :", flatSlides);

    return (
        <View>
            <FlatList
                data={flatSlides}
                horizontal
                pagingEnabled
                showsHorizontalScrollIndicator={false}
                bounces={false}
                keyExtractor={(item, index) => index.toString()}
                renderItem={({ item }) => {
                    console.log("Photo en cours de rendu :", item.photos);
                    return (
                        <View style={styles.container}>
                            
                            
                            <Image
                                source={{ uri: item.photos }}
                                style={styles.photosimages}
                                onError={() => console.log("Erreur de chargement pour :", item.photos)}
                            />
                            
                            
                        </View>
                    );
                }}
            />
        </View>
    );
};

export default ImageDetails;

const styles = StyleSheet.create({
    container:{
      flex: 1,
      justifyContent:'center',
      alignItems:"center",
      
    },
    photosimages: {
        height: 900,
        width: 410,
        resizeMode: 'cover',
    },
   
});
