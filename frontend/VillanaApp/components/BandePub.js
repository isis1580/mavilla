import { StyleSheet, Text, View, FlatList, TouchableOpacity, Image, Linking } from 'react-native';
import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import { useNavigation } from '@react-navigation/native';
import Config from './Config';

const BandePub = () => {
    const [ads, setAds] = useState([]);
    const navigation = useNavigation();
    const flatListRef = useRef(null); // Référence à la FlatList
    const [currentIndex, setCurrentIndex] = useState(0); // Index actuel

    useEffect(() => {
        const fetchData = async () => {
            try {
                const adsResponse = await axios.get(`http://${Config.serverIp}/publicites/`);
                setAds(adsResponse.data);
            } catch (error) {
                console.error('Erreur lors du fetch:', error);
            }
        };

        fetchData();
    }, []);

    useEffect(() => {
        const interval = setInterval(() => {
            setCurrentIndex((prevIndex) => {
                const nextIndex = (prevIndex + 1) % ads.length; // Boucle à travers les éléments
                flatListRef.current.scrollToIndex({ index: nextIndex, animated: true }); // Défilement vers l'index suivant
                return nextIndex;
            });
        }, 3000);

        return () => clearInterval(interval);
    }, [ads]);

    const handlePress = (ad) => {
        if (ad.lien) {
            Linking.openURL(ad.lien);
        } else {
            alert("Aucun lien disponible pour cette publicité.");
        }
    };

    return (
        <View>
            <FlatList
                ref={flatListRef} 
                data={ads}
                keyExtractor={item => item.id.toString()}
                horizontal
                showsHorizontalScrollIndicator={false}
                renderItem={({ item }) => {
                    return (
                        <View style={styles.container}>
                            <TouchableOpacity onPress={() => navigation.navigate('HotelsDetails',{trip:item})}>
                                <View  style={styles.Imagecontainer}>
                                    <Image
                                        source={{ uri: item.photos }}
                                        style={styles.BandePubImage}
                                        onError={() => console.log("Erreur de chargement de l'image:", item.image)}
                                        defaultSource={require('../assets/icon.png')}
                                    />
                                    
                                </View>
                            </TouchableOpacity>
                        </View>
                    );
                }}
            />
        </View>
    );
};

export default BandePub;

const styles = StyleSheet.create({

    container:{
        flex: 1,
        resizeMode: 'contain',

    },
    BandePubImage: {
        width: 350,
        height: 180,
        resizeMode: 'contain',
        borderRadius: 20,
    },
    
    Imagecontainer:{
        backgroundColor:'#fff',
        width: 350,
        height: 180,
        resizeMode: 'contain',
        borderRadius: 20,
        marginHorizontal: 10,
    }
});