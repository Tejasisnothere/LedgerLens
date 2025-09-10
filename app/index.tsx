import "../global.css"
import { Redirect, Stack } from 'expo-router'
import { useAuth } from '@clerk/clerk-expo'

export default function AuthRoutesLayout() {
    const { isSignedIn } = useAuth()

    if (isSignedIn) {
        return <Redirect href={'/(root)/(tabs)/home'} />
    }

    return <Redirect href={'/(auth)/welcome'} />
}