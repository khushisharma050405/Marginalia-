"use client";
import {useEffect} from "react";import {useRouter} from "next/navigation";
export default function P(){const r=useRouter();useEffect(()=>{r.replace(localStorage.getItem("token")?"/home":"/login")},[]);return null}
