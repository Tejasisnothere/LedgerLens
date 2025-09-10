import {Image, ScrollView, Text, View} from "react-native";
import InputField from "@/components/InputField"
import {useState} from "react";
import {icons} from "@/constants";
import CustomButton from "@/components/CustomButton";
import {Link} from "expo-router";
import OAuth from "@/components/OAuth";

const SignUp = () => {

    const [form, setForm] = useState({
        email: "",
        password: ""
    });

    const onSignInPress = async () => {

    }
    return (
        <ScrollView className={"flex-1 bg-white"}>
            <View className={"flex-1 bg-white"}>
                <View>
                    <Image
                        source={require("../../assets/images/signup-car.png")}
                        className={"z-0 w-full h-[250px]"}
                    />
                    <Text className={"text-2xl text-black font-JakartaSemiBold absolute bottom-5 left-5"}>Welcome back</Text>
                </View>
                <View className={"p-5"}>
                    <InputField
                        label={"Email"}
                        placeholder={"Enter your email"}
                        icon={icons.email}
                        value={form.email}
                        onChangeText={(value) => setForm({ ...form, email: value })}
                    />
                    <InputField
                        label={"Password"}
                        placeholder={"Enter your password"}
                        icon={icons.lock}
                        value={form.password}
                        onChangeText={(value) => setForm({ ...form, password: value })}
                        secureTextEntry={true}
                    />

                    <CustomButton
                        title={"Login"}
                        onPress={() => {onSignInPress}}
                        className={"mt-6"}
                    />

                    <OAuth/>

                    <Link href={"/sign-up"} className={"text-lg text-center text-general-200 mt-10"}>
                        <Text>Don't have an account? </Text>
                        <Text className={"text-primary-500"}>Sign up</Text>
                    </Link>
                </View>

                {/* Verification model */}

            </View>
        </ScrollView>
    );
}

export default SignUp;