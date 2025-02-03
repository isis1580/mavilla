import React, { useEffect, useState } from 'react';
import { StyleSheet, Text, View, FlatList, TouchableOpacity, Image, Alert } from 'react-native';
import { FontAwesome } from '@expo/vector-icons';
import axios from 'axios';
import { useNavigation } from '@react-navigation/native';

const serverIp = '10.125.9.182:8000';

const BandeMaisons = () => {
    const navigation = useNavigation();
    const [maisons, setMaisons] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(`http://${serverIp}/maisons/`);
                console.log("Données récupérées :", response.data);
                setMaisons(response.data);
            } catch (error) {
                console.error('Erreur lors du fetch:', error);
            }
        };

        fetchData();
    }, []);

    const renderMaisonItem = ({ item }) => {
        console.log("Données de la maison :", item);
    
        // Construction de l'URL de l'image
        const imageUri = item.photos[0]?.photos;
    
        console.log("Image URI:", imageUri); // Ajoutez cette ligne pour déboguer
    
        return (
            <TouchableOpacity onPress={() => navigation.navigate('HotelsDetails', { trip: item })}>
                <View>
                    <View style={styles.Imagebox}>
                        {imageUri ? (
                            <Image
                                source={{ uri: imageUri }}
                                onError={() => console.log("Erreur de chargement de l'image:", imageUri)}
                                defaultSource={require('../assets/icon.png')}
                                style={styles.maisonImage}
                            />
                        ) : (
                            <Image
                                source={require('../assets/icon.png')}
                                style={styles.maisonImage}
                            />
                        )}
                        <View style={styles.first}>   
                            <Text style={styles.maisonText}>{item.prix} fCfa</Text>      
                        </View>
                    </View>
    
                    <View style={styles.DetailText}>
                        <View>
                            <TouchableOpacity onPress={() => navigation.navigate('ProfilScreen')}>          
                                <Image source={require('../assets/profil.jpg')} style={styles.Userprofil} />
                            </TouchableOpacity>
                        </View>
                        <View style={styles.bottomview}>
                            <Text style={styles.Text1}>{item.ville}/{item.quartier}</Text> 
                            <View style={styles.heartview}>
                                <FontAwesome name="heart" size={25} color={'red'} />
                            </View>
                        </View>
                    </View>
                </View>
            </TouchableOpacity>
        );
    };

    return (
        <View style={styles.container}>
            <Text style={styles.title}>A Vendre</Text>
            <FlatList
                data={maisons.filter(maison => maison.type_maison === 'vente')}
                keyExtractor={item => item.id.toString()}
                horizontal
                showsHorizontalScrollIndicator={false}
                renderItem={renderMaisonItem}
            />
            <Text style={styles.title}>Location</Text>
            <FlatList
                data={maisons.filter(maison => maison.type_maison === 'location')}
                keyExtractor={item => item.id.toString()}
                horizontal
                showsHorizontalScrollIndicator={false}
                renderItem={renderMaisonItem}
            />
        </View>
    );
};

export default BandeMaisons;

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        marginLeft: 15,
        marginTop: 20,
        marginBottom: 15,
    },
    maisonContainer: {
        marginRight: 10,
        alignItems: 'center',
    },
    maisonImage: {
        width: 300,
        height: 170,
        resizeMode: 'cover',
        borderTopLeftRadius: 20,
        borderTopRightRadius: 20,
        marginLeft: 15,
    },
    maisonText: {
        color: '#444',
        marginTop: 5,
        textAlign: 'center',
        fontWeight: 'bold'
    },
    Imagebox: {
        overflow: 'hidden',
    },
    first: {
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'space-between',
        paddingHorizontal: 10,
        position: 'absolute',
        top: 10,
        left: 20,
        backgroundColor: '#fff',
        borderRadius: 20,
    },
    Text1: {
        fontSize: 15,
        fontWeight: 'bold',
        color: '#444',
        marginRight: 10,
        justifyContent: 'center'
    },
    Userprofil: {
        width: 40,
        height: 40,
        borderRadius: 50,
        backgroundColor: '#fff',
        borderWidth: 1,
        borderColor: '#e3e9ee',
        alignItems: 'center',
        justifyContent: 'center'
    },
    DetailText: {
        backgroundColor: '#fff',
        width: 300,
        marginLeft: 15,
        height: 50,
        borderBottomLeftRadius: 20,
        borderBottomRightRadius: 20,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingHorizontal: 10,
    },
    bottomview: {
        flexDirection: 'row',
        alignItems: 'center',
    },
    heartview: {
        width: 40,
        height: 40,
        borderRadius: 50,
        backgroundColor: '#fff',
        borderWidth: 1,
        borderColor: '#e3e9ee',
        alignItems: 'center',
        justifyContent: 'center'
    }
});