import { StyleSheet, Text, View, FlatList, TouchableOpacity, Image, Alert } from 'react-native';
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigation } from '@react-navigation/native';
import Config from './Config';
import { FontAwesome } from '@expo/vector-icons';

const BandeParcelle = () => {
    const [parcelles, setParcelles] = useState([]);
    const navigation = useNavigation();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const parcellesResponse = await axios.get(`http://${Config.serverIp}/parcelles/`);
                console.log(parcellesResponse.data);
                setParcelles(parcellesResponse.data);
            } catch (error) {
                console.error('Erreur lors du fetch:', error);
            }
        };

        fetchData();
    }, []);


    return (
        <View>
            <Text style={styles.title}>Terrains</Text>
            <FlatList
                data={parcelles}
                keyExtractor={item => item.id.toString()}
                horizontal
                showsHorizontalScrollIndicator={false}
                renderItem={({ item }) => {
                    const imageUri = item.photos[0]?.photos; // Accéder à la première image
                
                    return (
                        <View>
                            
                            <TouchableOpacity onPress={() => navigation.navigate('HotelsDetails',{trip:item})}>
                                <View style={styles.container}>
                                    {imageUri ? (
                                        <Image
                                            source={{ uri: imageUri }}
                                            onError={() => console.log("Erreur de chargement de l'image:", imageUri)}
                                            defaultSource={require('../assets/icon.png')}
                                            style={styles.ParcelleImage}
                                        />
                                    ) : (
                                        <Image
                                            source={require('../assets/icon.png')}
                                            style={styles.ParcelleImage}
                                        />
                                    )}
                                    <View style={styles.Titlebox1}>
                                        <View style={styles.first}>
                                            <View >
                                            <TouchableOpacity onPress={() => navigation.navigate('ProfilScreen')}>          
                                                <Image source={require('../assets/profil.jpg')} style={styles.Userprofil}
                                                />
                                            </TouchableOpacity>
                                            </View>
                                            <Text style={styles.Text1}>{item.surface}m2/{item.quartier}</Text> 
                                        </View>
                                        <View >
                                            <FontAwesome name= "heart" size={25} color="#fff" borderColor="#fff" />
                                        </View>
                                    </View>
                                </View>
                            </TouchableOpacity>
                        </View>
                    );
                }}
            />
            <View style={styles.buttonview}>
                <TouchableOpacity style={styles.button} >
                        <Text style={styles.buttonText}>Tout Voir </Text>
                </TouchableOpacity>
            </View>
        </View>
    );
};

export default BandeParcelle;

const styles = StyleSheet.create({
    container:{

    },
    ParcelleImage: {
        width: 370,
        height: 250,
        resizeMode: 'cover',
        borderRadius: 20,
        marginHorizontal: 10,
    },
    Titlebox: {
        position: 'absolute',
        bottom: 10,
        left: 10,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        padding: 5,
        borderRadius: 20,
    },
    title: {
        fontSize: 25,
        fontWeight: 'bold',
        marginLeft:15,
        marginBottom:20
    },
    Text1: {
        fontSize: 20,
        fontWeight: 'bold',
        color: '#fff',
        marginLeft:5
    },
    Titlebox1:{
        position: 'absolute',
        bottom: 20,
        flexDirection:'row',
        justifyContent: 'space-between',
        width:'100%',
        paddingHorizontal: 25,
        alignItems:'center'

    }, 
    Userprofil:{

        width: 40,
        height: 40,
        borderRadius: 50,
        backgroundColor: '#fff',
        borderWidth: 1,
        borderColor: '#e3e9ee',
        alignItems:'center',
        justifyContent:'center'

    },
    first:{
        flexDirection:'row',
        alignItems:'center',
        justifyContent:'center'
    },

    Likeicon:{

        width: 40,
        height: 40,
        borderRadius: 50,
        backgroundColor: '#fff',
        borderWidth: 1,
        borderColor: '#e3e9ee',
        alignItems:'center',
        justifyContent:'center'

    },
    
    button:{
        marginTop: 20,
        backgroundColor:'grey',
        justifyContent:'center',
        alignItems:'center',
        borderRadius: 15,
        alignSelf: 'flex-start',
        marginLeft:10,
        padding:5,
        marginBottom:100

    },
    buttonText:{
        fontSize:20,
        color: 'white'
        
    },
    buttonview:{
        flexDirection:'row',
        justifyContent:'center',
        alignContent:'center',

    }
});