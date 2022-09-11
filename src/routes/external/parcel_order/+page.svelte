<script lang="ts">
	import { Button, Column, Row } from 'carbon-components-svelte';
	import ParcelOrderForm from '$lib/components/ParcelOrderForm.svelte';
	import { v4 as uuidv4 } from 'uuid';

	let full_name: string;
	let pickup_location: string;
	let destination_location: string;
	let order_id: string;
	let response_status: number = 0;
	let cost: number = 0;
	$: order_success = response_status == 202 ? true : false;

	const coordinates = {
		London: { LAT: 51.5007, LON: 0.1246 },
		Paris: { LAT: 48.8584, LON: 2.2945 },
		Chicago: { LAT: 41.8919, LON: 87.6051 },
		Boston: { LAT: 42.3467, LON: 71.0972 },
		Seattle: { LAT: 47.6205, LON: 122.3493 }
	};

	const costs = {
		London: {
			Paris: 30,
			Chicago: 130,
			Boston: 90,
			Seattle: 250
		},
		Paris: {
			London: 30,
			Chicago: 160,
			Boston: 120,
			Seattle: 280
		},
		Chicago: {
			Paris: 160,
			London: 130,
			Boston: 60,
			Seattle: 150
		},
		Boston: {
			Paris: 120,
			Chicago: 60,
			London: 90,
			Seattle: 190
		},
		Seattle: {
			Paris: 280,
			Chicago: 150,
			Boston: 190,
			London: 250
		}
	};

	function submit_callback() {
		const pickup_coords = coordinates[pickup_location];
		const destination_coords = coordinates[destination_location];
		const current_time = new Date(new Date().getTime()).toISOString();
		order_id = uuidv4();
		const order_event = {
			customer_name: full_name,
			order_id: order_id,
			pickup_coords: Object.values(pickup_coords).join(','),
			pickup_location: pickup_location,
			destination_coords: Object.values(destination_coords).join(','),
			destination_location: destination_location,
			event_ts: current_time,
			time_ordered: current_time,
			order_cost: cost
		};
		fetch('https://api.tinybird.co/v0/events?name=parcel_order_events', {
			method: 'POST',
			body: JSON.stringify(order_event),
			headers: {
				Authorization:
					'Bearer p.eyJ1IjogImQwZWIyNzhmLTk4ZTQtNDMxNC1hMDMzLWM0OTBkZDU1ODQ0MCIsICJpZCI6ICI0NzQzZWRkYy02MzA4LTQ1MDUtOTc1YS1lZmIzMjQ1M2ZjNGYifQ.fCQZ6HYusIX9IfS3YRTLZOjxbwi9GSjyTA7uS6WoCB4'
			}
		}).then((res) => {
			response_status = res.status;
		});
	}

	function destination_change() {
		cost = costs[pickup_location][destination_location];
	}

	function reset() {
		full_name = undefined;
		pickup_location = undefined;
		destination_location = undefined;
		response_status = 0;
		order_id = undefined;
		cost = 0;
	}
</script>

{#if !order_success}
	<Row>
		<Column lg={{ span: 4, offset: 6 }}>
			<!-- <Column > -->
			<h1>Parcel Order Form</h1>
			<ParcelOrderForm
				on:change={destination_change}
				on:click={submit_callback}
				bind:full_name
				bind:pickup_location
				bind:destination_location
				{cost}
			/>
		</Column>
	</Row>
{:else if order_success}
	<Row>
		<Column lg={{ span: 8, offset: 4 }}>
			<!-- <Column > -->
			<h1>Order successful!</h1>
			<h3>Your Order ID</h3>
			<h4>{order_id}</h4>
		</Column>
	</Row>
	<Row>
		<Column lg={{ span: 2, offset: 7 }}>
			<Button on:click={reset}>Reset</Button>
		</Column>
	</Row>
{/if}

<style>
	h1,
	h3,
	h4 {
		text-align: center;
		padding-bottom: 1rem;
	}
</style>
