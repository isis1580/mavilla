import { StyleSheet, Text, View, FlatList, TouchableOpacity, Image } from 'react-native'; 
import React, { useEffect, useState } from 'react';
import axios from 'axios'; 
import { FontAwesome } from '@expo/vector-icons'; 
import { useNavigation } from '@react-navigation/native';  
import Config from './Config';
import { SharedElement } from 'react-navigation-shared-element';

const BandeHotels = () => {
    const [hotels, setHotels] = useState([]);
    const navigation = useNavigation();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const hotelsResponse = await axios.get(`http://${Config.serverIp}/hotels/`);
                console.log('Réponse de l\'API:', hotelsResponse.data); 
                setHotels(hotelsResponse.data);
            } catch (error) {
                console.error('Erreur lors du fetch:', error);
            }
        };
    
        fetchData();
    }, []);

    return (
        <View>
            
            <View style={styles.buttonview}>
                <Text style={styles.title}>Terrains</Text>
                <TouchableOpacity style={styles.button}>
                        <Text style={styles.buttonText}>Tout Voir</Text>
                </TouchableOpacity>
            </View>
            <FlatList
                data={hotels}
                keyExtractor={item => item.id.toString()}
                horizontal
                showsHorizontalScrollIndicator={false}
                renderItem={({ item }) => {
                    console.log('Élément de l\'hôtel:', item);
                    return (
                        <TouchableOpacity onPress={() => {navigation.navigate('HotelsDetails', { 
                                            trip: item
                                            }); }}>    
                            <View>    
                                <SharedElement id={`trip.${item.id}.photos`}> 
                                    <View style={[styles.Imagebox]}>
                                        <Image
                                            source={{ uri: item.photos[0]?.photos }}
                                            onError={() => console.log("Erreur de chargement de l'image:", item.photos[0]?.photo)}
                                            defaultSource={require('../assets/icon.png')}
                                            style={styles.HotelImage}
                                        />
                                        <View style={styles.Titlebox}>
                                            <Text style={styles.Text1}>{item.titre}</Text>
                                        </View>
                                    </View>
                                </SharedElement>     
                                <View style={styles.DetailText}>
                                    <View style={styles.startview}>
                                        <FontAwesome name="star" size={15} color="#e79d3f" />
                                        <FontAwesome name="star" size={15} color="#e79d3f" />
                                        <FontAwesome name="star" size={15} color="#e79d3f" />
                                        <FontAwesome name="star" size={15} color="#e79d3f" />
                                        <FontAwesome name="star" size={15} color="#e79d3f" />
                                    </View>
                                    <Text>Voir</Text>
                                </View>
                                
                            </View>     
                        </TouchableOpacity>
                    );
                }}
            />
            
            
        </View>
    );
};

export default BandeHotels;

const styles = StyleSheet.create({
    HotelImage: {
        width: 180,
        height: 210,
        resizeMode: 'cover',
        borderTopLeftRadius: 20,
        borderTopRightRadius: 20,
        marginLeft: 15,
    },
    Titlebox: {
        position: 'absolute',
        top: 10,
        left: 20,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        borderRadius: 20,

    },
    title: {
        fontSize: 25,
        fontWeight: 'bold',
    },
    Text1: {
        fontSize: 20,
        fontWeight: 'bold',
        color: '#fff',
        padding:5
    },
    button:{
        backgroundColor:'green',
        justifyContent:'center',
        alignItems:'center',
        borderRadius: 15,
        alignSelf: 'flex-end',


    },
    buttonText:{
        fontSize:20,
        color: 'white',
        padding:5,
        
        
    },
    buttonview:{
        flexDirection:'row',
        justifyContent:'space-between',
        alignContent:'center',
        paddingHorizontal:20,
        marginBottom:20

    },
    DetailText: {
        backgroundColor: '#fff',
        width: 180,
        marginLeft: 15,
        height: 50,
        borderBottomLeftRadius: 20,
        borderBottomRightRadius: 20,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingHorizontal: 10,
    },
    startview: {
        flexDirection: 'row',
    },
    Imagebox: {
        overflow: 'hidden',
    },
});