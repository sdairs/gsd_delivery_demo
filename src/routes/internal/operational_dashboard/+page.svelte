<script lang="ts">
	import Metric from '$lib/components/dashboard/Metric.svelte';
	import { Column, Row, Tile, Select, SelectItem } from 'carbon-components-svelte';
	import { PieChart, AreaChart } from '@carbon/charts-svelte';
	import { onMount } from 'svelte';

	let token: string | null;
	onMount(() => {
		token = new URL(document.location).searchParams.get('token');
	});

	let time_range_minutes: number = 5;

	let parcel_metrics: object = {
		ordered: 0,
		collected: 0,
		at_depot: 0,
		with_driver: 0,
		delivered: 0
	};

	let parcel_metrics_pie_ordered_vs_delivered: Array<object> = [
		{ group: 'Ordered', value: 0 },
		{ group: 'Delivered', value: 0 }
	];
	let parcel_metrics_pie_in_vs_out: Array<object> = [
		{ group: 'Collected', value: 0 },
		{ group: 'With Driver', value: 0 }
	];

	$: {
		parcel_metrics;
		parcel_metrics_pie_ordered_vs_delivered = [];
		parcel_metrics_pie_ordered_vs_delivered.push({
			group: 'Ordered',
			value: parcel_metrics['ordered']
		});
		parcel_metrics_pie_ordered_vs_delivered.push({
			group: 'Delivered',
			value: parcel_metrics['delivered']
		});
		parcel_metrics_pie_in_vs_out = [];
		parcel_metrics_pie_in_vs_out.push({ group: 'Collected', value: parcel_metrics['collected'] });
		parcel_metrics_pie_in_vs_out.push({
			group: 'With Driver',
			value: parcel_metrics['with_driver']
		});
	}

	let parcels_ordered_today: Array<object> = [];

	async function get_parcels_metrics(status: string) {
		let params = new URLSearchParams({ status: status, interval: time_range_minutes });
		let url = new URL('https://api.tinybird.co/v0/pipes/get_parcel_metrics.json?' + params);

		const result = await fetch(url, {
			headers: {
				Authorization:
					'Bearer ' +
					(token == null
						? 'p.eyJ1IjogImQwZWIyNzhmLTk4ZTQtNDMxNC1hMDMzLWM0OTBkZDU1ODQ0MCIsICJpZCI6ICJhMDJkZDgxNS0zM2MyLTRkNWQtODE5Yy02MDk5MTc3YTg4OTIifQ.G37JBZ8EO-OiN9PUQXuvWx1g7vtFn1LZWRUAqFKts6Y'
						: token)
			}
		})
			.then((r) => r.json())
			.then((r) => r)
			.catch((e) => e.toString());
		parcel_metrics[status] = result['data'][0]['total'];
	}

	async function get_parcels_ordered_over_time() {
		let params = new URLSearchParams({ interval: time_range_minutes });
		let url = new URL('https://api.tinybird.co/v0/pipes/parcels_ordered_over_time.json?' + params);

		const result = await fetch(url, {
			headers: {
				Authorization:
					'Bearer ' +
					(token == null
						? 'p.eyJ1IjogImQwZWIyNzhmLTk4ZTQtNDMxNC1hMDMzLWM0OTBkZDU1ODQ0MCIsICJpZCI6ICI4YmY4ODI2MC1mMzY3LTQ3ZDgtODA5Mi01NGMzOGE0YzgyNDAifQ.XbZkDGOJzjIdvQ-yZBNv5rGsBOHLYb1d4ZqsqhBel2g'
						: token)
			}
		})
			.then((r) => r.json())
			.then((r) => r)
			.catch((e) => e.toString());
		parcels_ordered_today = result['data'];
	}

	function get_data() {
		get_parcels_metrics('ordered');
		get_parcels_metrics('collected');
		get_parcels_metrics('at_depot');
		get_parcels_metrics('with_driver');
		get_parcels_metrics('delivered');
		get_parcels_ordered_over_time();
	}
	get_data();
</script>

<Row>
	<Column lg={{ span: 6, offset: 5 }}>
		<h1>Operational Dashboard</h1>
	</Column>
</Row>
<Row>
	<Column lg={{ span: 8, offset: 4 }}>
		<Select labelText="Time Range" on:change={get_data} bind:selected={time_range_minutes}>
			<SelectItem value="5" text="5 Minutes" />
			<SelectItem value="15" text="15 Minutes" />
			<SelectItem value="30" text="30 Minutes" />
			<SelectItem value="60" text="1 Hour" />
			<SelectItem value="720" text="12 Hours" />
			<SelectItem value="1440" text="1 Day" />
			<SelectItem value="10080" text="7 Days" />
		</Select>
	</Column>
</Row>
<Row>
	<Column lg={{ span: 8, offset: 4 }}>
		<Row padding>
			<Column><Metric title={'Ordered'} metric={parcel_metrics['ordered']} /></Column>
			<Column><Metric title={'Delivered'} metric={parcel_metrics['delivered']} /></Column>
		</Row>
		<Row padding>
			<Column><Metric title={'Collected'} metric={parcel_metrics['collected']} /></Column>
			<Column><Metric title={'At Depot'} metric={parcel_metrics['at_depot']} /></Column>
			<Column><Metric title={'With Driver'} metric={parcel_metrics['with_driver']} /></Column>
		</Row>
		<Row padding>
			<Column lg={{ span: 8 }}>
				<Tile>
					<PieChart
						theme="g90"
						data={parcel_metrics_pie_ordered_vs_delivered}
						options={{
							height: '400px',
							toolbar: { enabled: false },
							pie: {
								alignment: 'center'
							},
							title: 'Ordered Vs Delivered',
							resizable: true,
							data: {
								loading: false
							},
							color: {
								scale: {
									Ordered: '#631D76',
									Delivered: '#9E4770'
								}
							}
						}}
					/>
				</Tile>
			</Column>
			<Column lg={{ span: 8 }}>
				<Tile>
					<PieChart
						theme="g90"
						data={parcel_metrics_pie_in_vs_out}
						options={{
							height: '400px',
							toolbar: { enabled: false },
							pie: {
								alignment: 'center'
							},
							title: 'In Vs Out',
							resizable: true,
							data: {
								loading: false
							},
							color: {
								scale: {
									Collected: '#6D9DC5',
									'With Driver': '#53599A'
								}
							}
						}}
					/>
				</Tile>
			</Column>
		</Row>
		<Row padding>
			<Column>
				<Tile>
					<AreaChart
						theme="g90"
						data={parcels_ordered_today}
						options={{
							toolbar: { enabled: false },
							title: 'Parcel Order Volume',
							height: '150px',
							grid: {
								x: {
									enabled: false
								},
								y: {
									enabled: false
								}
							},
							axes: {
								bottom: {
									visible: false,
									title: 'Date',
									mapsTo: 'date',
									scaleType: 'time'
								},
								left: {
									visible: false,
									mapsTo: 'value',
									scaleType: 'linear'
								}
							},
							color: {
								gradient: {
									enabled: true
								}
							},
							points: {
								enabled: false
							},
							legend: {
								enabled: false
							}
						}}
					/>
				</Tile>
			</Column>
		</Row>
	</Column>
</Row>

<style>
	h1 {
		text-align: center;
		padding-bottom: 1rem;
	}
</style>
