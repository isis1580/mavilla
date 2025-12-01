import { StyleSheet, Text, View, TouchableOpacity } from 'react-native';
import React from 'react';

const SectionHeader = ({ title, buttonTitle = '', onPress }) => {
    return (
        <View style={styles.TextView}>
            <View style={styles.container}>
                <Text style={styles.title}>{title}</Text>
                <TouchableOpacity 
                    style={styles.button} 
                    onPress={onPress} // Utiliser la fonction onPress passée en props
                >
                    <Text style={styles.buttonText}>{buttonTitle}</Text>
                </TouchableOpacity>
            </View>
        </View>
    );
};

export default SectionHeader;

const styles = StyleSheet.create({
    container: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginLeft:5,
        marginTop: 10,
        marginBottom: 20,
        paddingHorizontal:5
    },
    title: {
        fontSize: 25,
        fontWeight: 'bold',
    },
    
    buttonText: {
        color: '#fff', // Couleur du texte
        fontSize: 20,
        padding:5
    },
    button:{
        borderRadius:10,
        backgroundColor:'grey'
    }
});