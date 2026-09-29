<script setup lang="ts">
    import { ref, onMounted } from "vue"
    import type { Input } from "../types"
    import { getErrorMessage } from "@/api"
    import { create, getLatest } from "../api"
    import Form from "./Form.vue"
    import { useRouter } from "vue-router"

    const errorMessage = ref("")
    const router = useRouter()

    const payslip = ref<Input>({
        date: new Date(),
        honkyu: 0,
        noryokukyu: 0,
        mibunkyu: 0,
        shokuji_teate: 0,
        kenkyuin_teate: 0,
        tsukin_teate: 0,
        jutaku_teate: 0,
        nitto_teate: 0,
        kekkin_koujo: 0,
        jitan_kyushutsu_teate: 0,
        shoyo: 0,
        shoyo_kakyu: 0,
        tokubetsu_kakyu: 0,
        tokushu_kinmu_teate: 0,
        sonota_shikyu: 0,

        kenko_hoken: 0,
        kosei_nenkin: 0,
        koyo_hoken: 0,
        kodomo_shienkin: 0,
        shotoku_zei: 0,
        jumin_zei: 0,
        senyukaihi: 0,
        shokuji_dai: 0,
        shataku_ryo: 0,
        ryohi: 0,
        seimei_hoken: 0,
        sonota_kojo: 0,
        nencho_kabusoku: 0,
    })

    async function submit() {
        try {
            const record = await create(payslip.value)

            if (record?.id) {
                alert("登録が完了いたしました！")
                await router.push(`/payslip/${record.id}`)
            }
        } catch (error) {
            errorMessage.value = getErrorMessage(error)
        }
    }

    onMounted(async () => {
        const latest = await getLatest();
        if (latest) {
            payslip.value = {
                ...latest,
                date: new Date(),
            }
        }
    })

</script>

<template>
    <Form 
        v-model="payslip"
        @submit="submit"
        :name-error="errorMessage"
    />

</template>